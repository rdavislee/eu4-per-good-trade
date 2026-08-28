// WHO SENDS THE PLAYER'S MERCHANTS? (user, 2026-08-27: "there shouldn't be vanilla placing at all")
//
// Every send_merchant command executes through vtable 0x1C4D6C8 slot +0x48 = 0x274180. The rogue
// opening placements (type 0 at bordeaux/valencia) arrive as mission ARRIVALS (0x25AD10), so the
// creator acts earlier -- either this command (creators: the two node-window UI sites, the country
// trade view, the silenced AI helper 0x1BE790, and an unnamed main-loop dispatcher 0x249120)