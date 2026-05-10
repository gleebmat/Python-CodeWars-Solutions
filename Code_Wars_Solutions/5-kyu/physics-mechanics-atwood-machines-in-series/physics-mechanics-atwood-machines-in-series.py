g = 9.80665
​
def eff_Mass(mass1, mass2):
    return 4 * mass1 * mass2 / (mass1 + mass2)
​
def atwood(masses):
    
    amount=len(masses)
    mass_right=masses[-1]
    for each in range(amount - 1, 0, -1):
        if each == 1:
            mass_left = masses[0]
            return g * (mass_right - mass_left) / (mass_left + mass_right)
        
        mass_left = masses[each - 1]
        mass_right = eff_Mass(mass_left, mass_right)