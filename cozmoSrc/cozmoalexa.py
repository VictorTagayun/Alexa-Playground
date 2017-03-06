from cozmohttpclient import CozmoHttpClient
import cozmo
import asyncio

class CozmoAlexa:

    def __init__(self):
        self._client = CozmoHttpClient()
        
    async def run(self, coz_conn:cozmo.conn.CozmoConnection):
        self._robot = await coz_conn.wait_for_robot()
        self._robot.set_robot_volume(1.0)

        await self.sayToAlexa("Alexa")
        await self.sayToAlexa("Open a.i. rivalry")
        await asyncio.sleep(5)
        await self.sayToAlexa("I am better a.i. than you")
        await self.listenToResponse()
        await self._robot.play_anim_trigger(cozmo.anim.Triggers.FailedToRightFromFace).wait_for_completed()
        

    async def sayToAlexa(self, msg):
        await self._robot.say_text(msg,
                                   use_cozmo_voice=False,
                                   duration_scalar=1.1,
                                   voice_pitch=0).wait_for_completed()

    async def listenToResponse(self):
        # mock waiting time, wait for reaction
        r = self._client.getMessage()
        t = len(r) * 0.1
        print("Wait time ", t)
        await asyncio.sleep(t)
    

def main():
    ca = CozmoAlexa()
    cozmo.setup_basic_logging()
    cozmo.connect(ca.run)

if __name__ == '__main__':
    main()
