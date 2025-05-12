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
*   User-friendly interface (assumed based on "Click Apply").
*   Includes presets for common modifications.

## Prerequisites

*   **Python 3.x:** Make sure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).
*   **Git (Optional):** Needed if you want to clone the repository using Git commands.

## Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone <repository_url> # Replace <repository_url> with the actual URL
    cd rcm # Or whatever the repository folder is named
    ```
    Alternatively, download the source code as a ZIP file and extract it.

2.  **(Optional but Recommended) Install Dependencies:** If the script has external libraries, list the command here (e.g., `pip install -r requirements.txt`). If not, you can omit this step or state "No external dependencies required."

## How to Run

1.  Navigate to the script's directory in your terminal or file explorer.
2.  Execute the Python script:
    ```bash
    python rcm.py # Or the actual name of the main Python file
    ```
    *(Note: If the script has a GUI, double-clicking the `.py` file might also work if your Python installation is configured correctly, but running from the command line is often more reliable for seeing potential errors.)*

## Usage Guide

1.  Run the script as described above. This should open the RCM interface.
2.  Select the cache file or preset you wish to apply.
3.  Select the replacement cache file (if not using a preset).
4.  Click the "Apply" button.
5.  **Crucially:** For changes to take effect in Roblox, you must either:
    *   Restart the Roblox client completely.
    *   Leave and rejoin the specific game you are in.

## Included Presets

Here are some pre-configured modifications available:

### 1. R6 "Noclip" (Visual/Physics Glitch)

*   **Effect:** Modifies standard R6 animation files (like walk, run, idle) to significantly offset the visual position of your character's Torso and Head from their actual physical hitbox (controlled by the HumanoidRootPart). This can allow your *visual* character model to pass through some walls in certain games.
*   **Mechanism:** It replaces default R6 animations with custom ones where the Torso/Head joints are animated far away from the HumanoidRootPart.
*   **Limitations:**
    *   **Does NOT work in every game.** Effectiveness depends heavily on the game's configuration.
    *   **Custom Animations:** Useless if the game forces its own custom R6/R15 animations.
    *   **Collision Settings:** Ineffective if the game enables specific collision checks (e.g., `RootPartCollision` property enabled for R6 characters).
    *   **Custom Cameras:** May cause disorientation if the game uses a custom camera script that strictly follows the Head's visual position. Your viewpoint could be stuck far away from your actual location.
    *   **This is NOT true noclip.** Your actual physics collision (HumanoidRootPart) remains in the original spot. You cannot *walk* through walls, only *appear* to.

### 2. R6 AirWalk

*   **Effect:** Modifies jump/fall animations to cause the character to slowly float upwards (approx. 40 studs) after initiating a jump. Once at the peak, the character becomes somewhat stable for walking in the air.
*   **Activation:** Jump to start ascending. **Crucial: Do NOT input any movement commands (WASD) while ascending, or you will likely fall and trip.**
*   **Observed Behavior:** Other players will see your character floating and walking in the air.
*   **Sub-Features (Resulting from Animation Swaps):**
    *   **Air Walk:** Jump and wait without moving to float up.
    *   **Super Jump (Glitch):** Requires specific timing - falling over (tripping) and equipping a tool just before hitting the ground *might* launch you upwards (highly inconsistent).
    *   **Fast Travel (Glitch):** Holding 'W' (forward) while jumping *might* propel you forward quickly during the ascent phase (inconsistent).
    *   **Wall Clip (Glitch):** Holding a movement key towards a thin wall (approx. 1-10 studs) and jumping *might* cause your character's physics to glitch through upon landing or during ascent (highly inconsistent).

## Upcoming Features

*   Expanding the library of built-in presets and easily swappable cache files.
*   Improved handling and identification for non-animation cache types (textures, sounds, meshes).
*   General usability improvements and additional modification functions.
*   [Add any other specific planned features here]

---

**Remember the warning at the top. Use this tool responsibly and ethically.**
