from .ec import write

def apply_fan_profile(config):
    profile = config.get("PROFILE")
    on_off = [
        config.get("AUTO_ADV_VALUES"),
        config.get("COOLER_BOOSTER_OFF_ON_VALUES")
    ]
    # Note: The original code structure for ONOFF was a bit confusing.
    # Original:
    # fan_profile(1, [[config.AUTO_ADV_VALUES[0], config.AUTO_ADV_VALUES[1]], [config.COOLER_BOOSTER_OFF_ON_VALUES[0], config.COOLER_BOOSTER_OFF_ON_VALUES[1]]], ...)
    # Let's simplify based on the profile.

    address = config.get("CPU_GPU_FAN_SPEED_ADDRESS")
    
    if profile == 1: # Auto
        # Cooler Booster off
        write(on_off[1][0], on_off[1][1])
        # Auto mode on
        write(on_off[0][0], on_off[0][1])
        
        speeds = config.get("AUTO_SPEED")
        _write_speeds(address, speeds)

    elif profile == 2: # Basic
        # Cooler Booster off
        write(on_off[1][0], on_off[1][1])
        # Advanced mode on (Basic uses Advanced mode with offset)
        write(on_off[0][0], on_off[0][2])
        
        # Calculate basic speeds
        basic_speed = [[0]*7, [0]*7] # Placeholder, logic needs to be passed in or calculated
        # In original code, BASIC_SPEED was [[0...], [0...]] (all zeros)
        # and then speed_checker applied the offset.
        # But wait, if BASIC_SPEED is all zeros, then it's just the offset?
        # Original: speed_checker(BASIC_SPEED, offset)
        # If BASIC_SPEED is all 0, then the result is just the offset (clamped 0-150).
        # This seems to imply "Basic" mode sets a constant speed?
        # Or maybe BASIC_SPEED was supposed to be something else?
        # In original code: BASIC_SPEED = [[0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0]]
        # So yes, it seems it sets a constant speed based on offset?
        # Let's assume that for now.
        
        offset = config.get("BASIC_OFFSET")
        # Clamp offset
        if offset > 30: offset = 30
        if offset < -30: offset = -30
        
        speeds = [[0]*7, [0]*7]
        for r in range(2):
            for c in range(7):
                val = speeds[r][c] + offset
                val = max(0, min(150, val))
                speeds[r][c] = val
        
        _write_speeds(address, speeds)

    elif profile == 3: # Advanced
        # Cooler Booster off
        write(on_off[1][0], on_off[1][1])
        # Advanced mode on
        write(on_off[0][0], on_off[0][2])
        
        speeds = config.get("ADV_SPEED")
        _write_speeds(address, speeds)

    elif profile == 4: # Cooler Booster
        # Cooler Booster on
        write(on_off[1][0], on_off[1][2])

def _write_speeds(addresses, speeds):
    for row in range(2):
        for col in range(7):
            write(addresses[row][col], speeds[row][col])
