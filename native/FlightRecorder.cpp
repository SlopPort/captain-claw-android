// Local, bounded diagnostic flight recorder. OpenAI Codex (LLM).
#include "FlightRecorder.h"
#if defined(__ANDROID__) && !defined(NDEBUG)
#include "Engine/Actor/Components/PhysicsComponent.h"
#include "Engine/Actor/Components/AnimationComponent.h"
#include "Engine/Actor/Actor.h"
#include "Engine/Physics/ClawPhysics.h"
#include <array>
#include <vector>
#include <memory>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <fstream>
#include <sstream>
#include <cstdio>
#include <cstring>
#include <cmath>
#include <cstdint>

namespace {
constexpr unsigned capacity=600, maxContacts=8;
unsigned inputMask=0;
struct Contact {
    float nx=0,ny=0,left=0,top=0,right=0,bottom=0;
    int type=0;
    bool enabled=false,touching=false,sensor=false,heroIsA=false;
};
struct Record {
    Uint32 tick=0,step=0;
    int level=0,feet=0;
    float x=0,y=0,vx=0,vy=0,physicsMs=0;
    unsigned keys=0,flags=0,totalContacts=0,savedContacts=0;
    char animation[48]{};
    std::array<Contact,maxContacts> contacts{};
};
struct Job {
    std::vector<Record> records;
    const char* reason="periodic";
    bool frozen=false;
};
class Recorder {
public:
    Recorder():enabled(!std::ifstream("flight-recorder-off").good()),session(SDL_GetPerformanceCounter()) {
        if(enabled) {
            try {worker=std::thread([this]{writeLoop();});}
            catch(const std::exception&) {enabled=false;SDL_LogWarn(SDL_LOG_CATEGORY_APPLICATION,"Pazur recorder: worker unavailable; disabled");}
        }
    }
    ~Recorder() {
        {std::lock_guard<std::mutex> lock(mutex);stopping=true;}
        wake.notify_one();
        if(worker.joinable()) worker.join();
    }
    void sample(b2Body* body,PhysicsComponent* pc,int level,Uint32 step) {
        if(!enabled || !body || !pc) return;
        const auto now=SDL_GetTicks();
        if(count && now-lastSample<100) return;
        lastSample=now;
        Record record;
        record.tick=now;record.step=step;record.level=level;record.keys=inputMask;
        const auto position=MetersToPixels(body->GetPosition()),velocity=body->GetLinearVelocity();
        record.x=position.x;record.y=position.y;record.vx=velocity.x;record.vy=velocity.y;
        record.physicsMs=body->GetWorld()->GetProfile().step;
        record.feet=pc->GetNumFootContacts();
        record.flags=(pc->IsOnGround()?1:0)|(pc->IsOnLadder()?2:0)|(pc->IsClimbing()?4:0)|
            (pc->IsFalling()?8:0)|(pc->IsJumping()?16:0);
        auto actor=static_cast<Actor*>(body->GetUserData());
        if(auto animation=actor->GetRawComponent<AnimationComponent>(false)) {
            const auto name=animation->GetCurrentAnimationName();
            std::snprintf(record.animation,sizeof(record.animation),"%s",name.c_str());
        }
        // Physical contacts first so sensors cannot crowd out a blocking wall.
        for(int pass=0;pass<2;++pass) for(auto edge=body->GetContactList();edge;edge=edge->next) {
            auto contact=edge->contact;
            const bool heroA=contact->GetFixtureA()->GetBody()==body;
            auto own=heroA?contact->GetFixtureA():contact->GetFixtureB();
            auto other=heroA?contact->GetFixtureB():contact->GetFixtureA();
            const bool sensor=own->IsSensor()||other->IsSensor();
            if(sensor!=(pass==1)) continue;
            ++record.totalContacts;
            if(record.savedContacts==maxContacts) continue;
            auto& value=record.contacts[record.savedContacts++];
            value.enabled=contact->IsEnabled();value.touching=contact->IsTouching();
            value.sensor=sensor;value.heroIsA=heroA;
            value.type=int(reinterpret_cast<std::intptr_t>(other->GetUserData()));
            const auto bounds=other->GetAABB(0);
            value.left=MetersToPixels(bounds.lowerBound.x);value.top=MetersToPixels(bounds.lowerBound.y);
            value.right=MetersToPixels(bounds.upperBound.x);value.bottom=MetersToPixels(bounds.upperBound.y);
            if(contact->GetManifold()->pointCount) {
                b2WorldManifold manifold;contact->GetWorldManifold(&manifold);
                value.nx=manifold.normal.x;value.ny=manifold.normal.y;
            }
        }
        ring[next]=record;next=(next+1)%capacity;if(count<capacity)++count;
        if(now-lastFlush>=5000) {queue(false,"periodic");lastFlush=now;}
        const bool horizontal=(inputMask&3)==1 || (inputMask&3)==2;
        const bool running=std::strstr(record.animation,"walk") || std::strstr(record.animation,"run") ||
            std::strstr(record.animation,"WALK") || std::strstr(record.animation,"RUN");
        // This is a candidate, not a bug verdict: intentionally pushing a wall
        // also meets these conditions. Retain history without altering physics.
        if(horizontal && running && (record.flags&1) && !(record.flags&6) &&
           std::fabs(record.x-previousX)<.5f && std::fabs(record.vx)<.05f) {
            if(!blockedSince) blockedSince=now;
            if(now-blockedSince>=750 && (!lastCandidate || now-lastCandidate>=15000)) {
                queue(true,"blocked-candidate");lastCandidate=now;
            }
        } else blockedSince=0;
        previousX=record.x;
    }
    void background() {if(enabled && count) queue(false,"background");}
private:
    void queue(bool frozen,const char* reason) {
        auto job=std::unique_ptr<Job>(new Job);job->reason=reason;job->frozen=frozen;
        job->records.reserve(count);
        for(unsigned i=0;i<count;++i) job->records.push_back(ring[(next+capacity-count+i)%capacity]);
        // Only one pending job per class: a slow/full disk cannot build an
        // unbounded queue. The worker never accesses actors or Box2D objects.
        {std::lock_guard<std::mutex> lock(mutex);
         (frozen?pendingEvent:pendingPeriodic)=std::move(job);}
        wake.notify_one();
    }
    bool write(const Job& job,unsigned slot) {
        const std::string target=std::string("flight-")+(job.frozen?"event-":"rolling-")+std::to_string(slot)+".txt";
        const auto temporary=target+".tmp";
        std::ofstream output(temporary,std::ios::binary|std::ios::trunc);
        output<<"Pazur flight recorder 1 build=0.4.35 session="<<session<<" reason="<<job.reason
              <<" samples="<<job.records.size()<<" capacity=600 contacts_per_sample=8\n";
        output<<"S tick level x y vx vy flags feet keys step_ms physics_ms animation contacts_total contacts_saved\n";
        output<<"C enabled touching sensor hero_is_a type nx ny left top right bottom\n";
        for(const auto& r:job.records) {
            output<<"S "<<r.tick<<' '<<r.level<<' '<<r.x<<' '<<r.y<<' '<<r.vx<<' '<<r.vy<<' '
                <<r.flags<<' '<<r.feet<<' '<<r.keys<<' '<<r.step<<' '<<r.physicsMs<<' '<<r.animation
                <<' '<<r.totalContacts<<' '<<r.savedContacts<<'\n';
            for(unsigned i=0;i<r.savedContacts;++i) {
                const auto& c=r.contacts[i];
                output<<"C "<<c.enabled<<' '<<c.touching<<' '<<c.sensor<<' '<<c.heroIsA<<' '<<c.type
                    <<' '<<c.nx<<' '<<c.ny<<' '<<c.left<<' '<<c.top<<' '<<c.right<<' '<<c.bottom<<'\n';
            }
        }
        output<<"end\n";output.close();
        if(!output || std::rename(temporary.c_str(),target.c_str())!=0) {
            std::remove(temporary.c_str());return false;
        }
        return true;
    }
    void writeLoop() {
        unsigned rollingSlot=0,eventSlot=0;bool reportedFailure=false;
        for(;;) {
            std::unique_ptr<Job> job;
            {std::unique_lock<std::mutex> lock(mutex);
             wake.wait(lock,[this]{return stopping||pendingEvent||pendingPeriodic;});
             if(pendingEvent) job=std::move(pendingEvent);
             else if(pendingPeriodic) job=std::move(pendingPeriodic);
             else if(stopping) break;}
            auto& slot=job->frozen?eventSlot:rollingSlot;
            bool success=false;
            try {success=write(*job,slot);} catch(const std::exception&) {success=false;}
            if(success) {slot^=1;reportedFailure=false;}
            else if(!reportedFailure) {
                SDL_LogWarn(SDL_LOG_CATEGORY_APPLICATION,"Pazur recorder: local write failed; gameplay continues");
                reportedFailure=true;
            }
        }
    }
    bool enabled=false,stopping=false;
    Uint64 session;
    std::array<Record,capacity> ring{};
    unsigned next=0,count=0;
    Uint32 lastSample=0,lastFlush=0,blockedSince=0,lastCandidate=0;
    float previousX=0;
    std::mutex mutex;
    std::condition_variable wake;
    std::unique_ptr<Job> pendingPeriodic,pendingEvent;
    std::thread worker;
};
std::unique_ptr<Recorder> recorder;
}
void PazurRecorder::Input(const SDL_Event& event) {
    if(event.type==SDL_APP_WILLENTERBACKGROUND ||
       (event.type==SDL_WINDOWEVENT && event.window.event==SDL_WINDOWEVENT_FOCUS_LOST)) {
        inputMask=0;if(recorder) recorder->background();return;
    }
    if(event.type!=SDL_KEYDOWN && event.type!=SDL_KEYUP) return;
    unsigned bit=0;
    switch(event.key.keysym.sym) {
      case SDLK_LEFT:bit=1;break;case SDLK_RIGHT:bit=2;break;
      case SDLK_UP:bit=4;break;case SDLK_DOWN:bit=8;break;
      case SDLK_SPACE:bit=16;break;case SDLK_LCTRL:bit=32;break;case SDLK_LALT:bit=64;break;
      default:return; // No text, names, arbitrary keyboard contents or device IDs.
    }
    if(event.type==SDL_KEYDOWN) inputMask|=bit;else inputMask&=~bit;
}
void PazurRecorder::Sample(b2Body* body,PhysicsComponent* pc,int level,Uint32 step) {
    if(!recorder) recorder.reset(new Recorder);
    recorder->sample(body,pc,level,step);
}
#else
void PazurRecorder::Input(const SDL_Event&) {}
void PazurRecorder::Sample(b2Body*,PhysicsComponent*,int,Uint32) {}
#endif
