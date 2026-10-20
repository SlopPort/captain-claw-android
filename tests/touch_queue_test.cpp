#include <cassert>
#include <queue>
#include "Engine/UserInterface/Touch/TouchEvents.h"

int main() {
    std::queue<Touch_Event> queue;
    SDL_TouchFingerEvent start{};
    start.fingerId = 17;
    start.x = 0.1f;
    start.y = 0.7f;
    SDL_TouchFingerEvent end = start;
    end.x = 0.4f;
    queue.push(Touch_Event(50, JOYSTICK_MOVE, Touch_JoystickEvent(start, end)));
    assert(queue.front().sdlEvent.user.data1 == &queue.front());
    Touch_Event event;
    event = queue.front();
    queue.pop();
    auto payload = static_cast<Touch_Event*>(event.sdlEvent.user.data1);
    assert(payload == &event);
    assert(payload->recognizerId == 50);
    assert(payload->customData.joystick.fingerId == 17);
    assert(payload->customData.joystick.dx > 0.29f);
    Touch_Event copied(event);
    assert(copied.sdlEvent.user.data1 == &copied);
}
