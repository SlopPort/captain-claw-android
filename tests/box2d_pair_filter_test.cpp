// Written by OpenAI Codex. Uses the project's pinned Box2D, not a replacement.
// Compare actual contact callback order, filtering calls and trajectories with
// the optimization enabled/disabled, including changes to body types/fixtures.
#include <Box2D/Box2D.h>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>

struct Listener : b2ContactListener {
    std::vector<std::string> events;
    void record(char kind,b2Contact* c) {
        events.push_back(std::string(1,kind)+":"+
            std::to_string(reinterpret_cast<intptr_t>(c->GetFixtureA()->GetUserData()))+":"+
            std::to_string(reinterpret_cast<intptr_t>(c->GetFixtureB()->GetUserData())));
    }
    void BeginContact(b2Contact* c) override { record('B',c); }
    void EndContact(b2Contact* c) override { record('E',c); }
    void PreSolve(b2Contact* c,const b2Manifold*) override { record('P',c); }
    void PostSolve(b2Contact* c,const b2ContactImpulse*) override { record('S',c); }
};
struct Filter : b2ContactFilter {
    int calls=0;
    bool ShouldCollide(b2Fixture* a,b2Fixture* b) override {
        ++calls;return b2ContactFilter::ShouldCollide(a,b);
    }
};
struct Scene {
    Listener listener;
    Filter filter;
    b2World world{b2Vec2(0,10)};
    std::vector<b2Body*> bodies;
    intptr_t nextId=1;
    b2Fixture* box(b2Body* body,float x,float y,float w,float h,bool sensor=false) {
        b2PolygonShape shape;shape.SetAsBox(w,h,b2Vec2(x,y),0);
        b2FixtureDef f;f.shape=&shape;f.density=1;f.isSensor=sensor;
        f.userData=reinterpret_cast<void*>(nextId++);
        return body->CreateFixture(&f);
    }
    b2Body* body(b2BodyType type,float x,float y) {
        b2BodyDef d;d.type=type;d.position.Set(x,y);
        auto b=world.CreateBody(&d);bodies.push_back(b);return b;
    }
    explicit Scene(bool optimized) {
        world.SetEarlyPairFiltering(optimized);
        world.SetContactListener(&listener);world.SetContactFilter(&filter);
        auto floor=body(b2_staticBody,0,5);
        // Adjacent tiles share a body, as in OpenClaw. Fat AABBs overlap.
        for(int i=0;i<100;++i)box(floor,float(i)-50,0,.5f,.5f);
        auto trigger=body(b2_staticBody,0,2);box(trigger,0,0,12,.3f,true);
        auto lift=body(b2_kinematicBody,0,3);box(lift,0,0,2,.2f);
        lift->SetLinearVelocity(b2Vec2(.5f,0));
        for(int i=0;i<20;++i) {
            auto b=body(b2_dynamicBody,float(i)-10,-float(i%3));
            box(b,0,0,.4f,.4f);box(b,0,.5f,.3f,.1f,true);
            b->SetBullet(i==0);
        }
        b2DistanceJointDef joint;
        joint.Initialize(bodies[3],bodies[4],bodies[3]->GetPosition(),bodies[4]->GetPosition());
        joint.collideConnected=false;world.CreateJoint(&joint);
    }
    void modify(int step) {
        // Duplicate touches can exceed the total proxy count without covering
        // all proxies. The subset optimization must not treat that as a full batch.
        if(step==5)for(int i=0;i<1000;++i)bodies[0]->GetFixtureList()->Refilter();
        if(step==30)box(bodies[5],.5f,0,.3f,.3f);
        if(step==40)bodies[6]->SetTransform(b2Vec2(0,-2),0);
        if(step==60)bodies[1]->SetType(b2_dynamicBody);
        if(step==80)bodies[2]->SetType(b2_dynamicBody);
        if(step==100)bodies[7]->SetType(b2_kinematicBody);
        if(step==120)bodies[8]->SetActive(false);
        if(step==130)bodies[8]->SetActive(true);
        if(step==150)bodies[5]->DestroyFixture(bodies[5]->GetFixtureList());
        if(step==180) { world.DestroyBody(bodies.back());bodies.pop_back(); }
        if(step==200) {
            auto f=bodies[9]->GetFixtureList();auto mask=f->GetFilterData();
            mask.maskBits=0;f->SetFilterData(mask);
        }
        if(step==220) {
            auto f=bodies[9]->GetFixtureList();auto mask=f->GetFilterData();
            mask.maskBits=0xffff;f->SetFilterData(mask);
        }
    }
};
int main() {
    Scene baseline(false),optimized(true);
    for(int step=0;step<600;++step) {
        baseline.modify(step);optimized.modify(step);
        const float dt=(step%3==0)?1.f/50:1.f/60;
        baseline.world.Step(dt,10,8);optimized.world.Step(dt,10,8);
        assert(baseline.listener.events==optimized.listener.events);
        assert(baseline.filter.calls==optimized.filter.calls);
        assert(baseline.world.GetContactCount()==optimized.world.GetContactCount());
        for(size_t i=0;i<baseline.bodies.size();++i) {
            const auto a=baseline.bodies[i],b=optimized.bodies[i];
            assert(a->GetPosition()==b->GetPosition());
            assert(a->GetLinearVelocity()==b->GetLinearVelocity());
            assert(a->GetAngle()==b->GetAngle());
            assert(a->GetAngularVelocity()==b->GetAngularVelocity());
            assert(a->IsAwake()==b->IsAwake());
        }
    }
    std::cout<<"PASS: 600 steps; identical trajectories, contact counts, ordered callbacks and filter calls; "
        <<optimized.listener.events.size()<<" callbacks\n";
}
