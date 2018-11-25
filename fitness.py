def evalFitness(candidate: BitStr, modulesTaken: MultiSet[FrozenSet[int]]) -> int:
    """candidate is a concatenation of all lectures."""
    sBits  = 1  # 0 == semester 1 else semester 2
    mdBits = 8  # bits encoding the module 2^8 = 256
    mBits  = 4  # bits encoding hours since 8am 2^4 = 16
    hBits  = 6  # bits encoding minutes 2^6 = 64
    dBits  = 3  # bits encoding day of the week 2^3 = 8
    lBits  = 8  # bits encoding int index in lecturers array 2^8 = 256
    lhBits = 8  # bits encoding int index in halls array 2^8 = 256
    subStrSize = sBits + mBits + hBits + dBits + lBits + lhBits + mdBits
    totalFitness = 0
    for lecture in candidate.split(subStrSize):
        fitness = 1000000  # initial fitness
        time = decodeTime(lecture)
        semester = lecture[0]
        lecturer = decodeLecturer(lecture)
        hall = decodeHall(lecture)
        module = decodeModule(lecture)
        if crossDepartament(lecturer, module):
            fitness -= 100
        for lecture2 in candidate.split(subStrSize):
            time2 = decodeTime(lecture2)
            semester2 = lecture2[0]
            lecturer2 = decodeLecturer(lecture2)
            hall2 = decodeHall(lecture2)
            if semester == semester2:
                if timesOverlap(time, time2):
                    if lecturer == lecturer2:
                        fitness -= 100
                    if hall == hall2:
                        fitness -= 100
                    for modules in modulesTaken.keys():
                        if module in modules:
                            noEnrollments = modulesTaken[module]
                            fitness -= noEnrollments * 100
        totalFitness += fitness
    return totalFitness
