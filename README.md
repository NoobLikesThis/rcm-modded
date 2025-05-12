# rcm
rcm, aka Roblox Cache Modifier is a python script to change any file that roblox caches (animations, textures, meshes and more)
these changes can not be detected by roblox (as of writing this)


## !!! WARNING !!!

This script modifies Roblox caches. Use it responsibly and understand the risks:

*   **User Assumes All Risk:** **YOU** are solely responsible for any consequences, including account warnings, suspensions, or bans from Roblox or specific games, that may result from using this script.
*   **No Liability:** The creator(s) of this script accept **NO liability** for any actions taken against your account(s).
*   **Not for Cheating:** Do not use this tool to violate rules or gain unfair advantages.

**Executing this script signifies your understanding and acceptance of these risks and your full responsibility.**



## How to run
1.  Clone the repo
2.  Double click the .py

## Usage
1. Click on cache or preset you want to replace
2. click Apply
3. Restart roblox / leave and rejoin game


## Upcoming features
*  More functions will be added soon
*  More Presets and preinstalled caches will be added soon
*  Added functionality for caches that are not animations (should work already but want to improve)

## Presets
*  # R6 "Noclip"
   *  This modifies the standard R6 animations to move your Torso and Head away from the real location, making you be able to walk through solid objects.
   *  This does not work in every roblox game, for one of the following:
      *  The game uses custom animations
      *  The game has RootPartCollision turned ON for R6
   *  It could also be that the game uses a custom camera, which locks to the head, making your POV always be high in the air
* # R6 AirWalk
   *  This slowly accends your character 40 studs into the sky after jumping. Do NOT move while character is moving up or else you could fall over
      *  Once fully accended, you should be semi-stable and be able to walk around. Other players will see you flying in the air
   *  # All functions of AirWalk:
      *  Air walk
         *  jump to start floating 40 studs into the sky. Do not move while moving up, else you will fall over
      *  Superjump
         *  fall over and equip tool before touching ground
      *  Fast travel
         *  hold w and jump
      *  Clip
         *  clip 1 - 100 stud walls by holding preferred movement key and jumping
