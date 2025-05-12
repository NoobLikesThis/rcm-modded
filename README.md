# RCM - Roblox Cache Modifier

**A Python script for swapping Roblox cached assets.**

---

**⚠️ IMPORTANT WARNING ⚠️**

This script modifies files within the Roblox cache directory. Using this tool carries inherent risks. Please read carefully:

*   **Use At Your Own Risk:** You, the user, assume **ALL responsibility** for any consequences that may arise from using this script. This includes, but is not limited to, warnings, suspensions, or bans issued by Roblox Corporation or individual game developers.
*   **No Liability:** The creator(s) of RCM accept **ZERO liability** for any negative actions taken against your Roblox account(s) as a result of using this tool.
*   **Intended Use:** This tool is provided for experimentation and customization purposes only. **Do NOT use it to gain unfair advantages, cheat, or violate Roblox's Terms of Service or any game's rules.**
*   **Undetectability Not Guaranteed:** While cache modification might be difficult to detect *currently* (May 2025), Roblox can change its detection methods at any time without notice. **Do not assume permanent undetectability.**

**By downloading, cloning, or executing this script, you acknowledge that you have read, understood, and accepted these terms and risks.**

---

## What is RCM?

RCM (Roblox Cache Modifier) is a Python script designed to easily swap assets stored in the Roblox cache. Roblox temporarily stores files like textures, sounds, meshes, and animations locally to speed up loading times. RCM allows you to replace one cached asset with another compatible asset file.

*   **Example:** You can replace the standard running animation cache file with a cache file of a different running animation.

Roblox typically stores its cache files here:
`%LOCALAPPDATA%\Temp\Roblox\http`

## Features

*   Modify cached assets like animations, textures, meshes, etc.
*   Clear http folder easily and fast
*   Includes presets.

## Prerequisites

*   **Python 3.x:** Make sure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).
*   **Git (Optional):** Needed if you want to clone the repository using Git commands.

## Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/vrbalxssandro/rcm.git
    ```
    Alternatively, download the source code as a ZIP file and extract it.

## How to Run

1.  Navigate to the script's directory in your terminal or file explorer.
2.  Execute the Python script:
    ```bash
    python rcm.py
    ```
    * Or just double click the Python file

## Usage Guide

1.  Run the script as described above. This should open the RCM interface.
2.  Select the cache file or preset you wish to apply.
3.  Click the "Apply" button.
4.  **Crucially:** For changes to take effect in Roblox, you must:
    *   Leave and rejoin the specific game you are in.

## Included Presets

Here are some pre-configured modifications available:

*  # R6 "Noclip"
   *  This modifies the standard R6 animations to move your Torso and Head away from the real location, making you be able to walk through solid objects.
   *  This does not work in every roblox game, for one of the following:
      *  The game uses custom animations
      *  The game has RootPartCollision turned ON for R6
   *  It could also be that the game uses a custom camera, which locks to the head, making your POV always be high in the air
* # R6 AirWalk
   *  This slowly accends your character 40 studs into the sky after jumping. Do NOT move while character is moving up or else you could fall over
      *  Once fully accended, you should be semi-stable and be able to walk around. Other players will see you flying in the air
   *  ### All functions of AirWalk:
      *  Air walk
         *  jump to start floating 40 studs into the sky. Do not move while moving up, else you will fall over
      *  Superjump
         *  fall over and equip tool before touching ground
      *  Fast travel
         *  hold w and jump
      *  Clip
         *  clip 1 - 100 stud walls by holding preferred movement key and jumping

## Upcoming Features

*   Expanding the library of built-in presets and easily swappable cache files.
*   Improved handling and identification for non-animation cache types (this should work already, but I want to make it easier, especially for textures).
*   General usability improvements and additional modification functions.

---

**Remember the warning at the top. Use this tool responsibly and ethically.**
