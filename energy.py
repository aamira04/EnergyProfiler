CPU_POWER_WATTS = 30  # simple assumption
def estimate_energy(cpu_time):
    return cpu_time * CPU_POWER_WATTS
