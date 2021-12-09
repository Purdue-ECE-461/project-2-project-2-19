# scoringscript.py>


def scoring(url, arg):
    active = None
    # weights for each score
    weight_ramp = 0.1
    weight_correct = 0.2
    weight_busfactor = 0.35
    weight_active = 0.2
    weight_license = 0.15

    # ramp up score checks if the repository has a readme, a contributing/issue template, and documentation to reduce
    # ramp-up time
    key = 'readme'
    key1 = 'contributing'
    key2 = 'documentation'
    unw_ramp = (arg.get(key) + arg.get(key1) + arg.get(key2)) / 3

    # correctness uses the average percentage of issues closed per month over the last three months (implemented)
    avg_iss_clsd = arg.get('average %issues closed')  # number of average issues closed
    if avg_iss_clsd == 0:
        correctness_sc = 0
    elif avg_iss_clsd <= 50:
        if avg_iss_clsd > 0:
            correctness_sc = 0.5
        else:
            correctness_sc = 0
    else:
        correctness_sc = 1

    # the number of contributors
    num_contributors = (arg.get('number_contributors'))
    if num_contributors >= 40:
        bus_score = 1
    elif 40 > num_contributors >= 20:
        bus_score = 0.5
    elif 20 > num_contributors >= 10:
        bus_score = 0.2
    elif num_contributors < 10:
        bus_score = 0
    else:
        bus_score = 0

    # active uses the average time taken to close or respond to an open issue over last month.
    time_taken = (arg.get('average time'))
    if time_taken:
        if time_taken <= 3:  # was chosen based on a an Audit by David Eaves for Mozilla Community Metrics. The
            # presentation is the first link for the search input: "Mozilla Community Metrics - Community Builders"
            active = 1
        elif 3 < time_taken <= 7:  # The same audit found that contributors who waited over 7 days for a code review had
            # virtually zero likelihood of returning, thus giving us the metric for active maintainers
            active = 0.4
        elif 7 < time_taken <= 50:
            active = 0.2
        elif time_taken > 50:
            active = 0
    else:
        active = 0
    # license checks if license is compatible with GNU LPGLv2.1
    license_boo = (arg.get('license'))  # gets value of key from dictionary input
    if license_boo == 0:  # All the pre-processing done in get-metadata.py. 1 if License is compatible with GNU
        # LGPLv2.1, 0 if it isn't.
        license_unw = 0
    else:
        license_unw = 1

    # assigning scores for clarity
    ramp_up_score = unw_ramp
    correctness_score = correctness_sc
    bus_factor_score = bus_score
    responsive_maintainer_score = active
    license_score = license_unw

    # Calculating weighted sum. Weights were assigned in a way that the sum is always between 0 and 1, with 0 for the
    # worst repositories and 1 for repositories that satisfy all requirements.
    net_score = (weight_ramp * ramp_up_score) + (weight_correct * correctness_score) + (
            weight_busfactor * bus_factor_score) + (weight_active * responsive_maintainer_score) + (
                        weight_license * license_score)
    net_score = round(net_score, 1)
    ramp_up_score = round(ramp_up_score, 1)
    correctness_score = round(correctness_score, 1)
    bus_factor_score = round(bus_factor_score, 1)
    responsive_maintainer_score = round(responsive_maintainer_score, 1)
    license_score = round(license_score, 1)

    print(f"{url} {net_score} {ramp_up_score} {correctness_score} {bus_factor_score} {responsive_maintainer_score}\
 {license_score}")
    pass
