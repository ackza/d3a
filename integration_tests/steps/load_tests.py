from behave import then
from pendulum.interval import Interval
from d3a.setup.strategy_tests import user_profile_load_csv, user_profile_load_dict # NOQA


@then('the DefinedLoadStrategy follows the Load profile provided as csv')
def check_load_profile_csv(context):
    house1 = next(filter(lambda x: x.name == "House 1", context.simulation.area.children))
    load = next(filter(lambda x: x.name == "H1 DefinedLoad", house1.children))
    input_profile = load.strategy._readCSV(user_profile_load_csv.profile_path)

    desired_energy = {f'{k.hour:02}:{k.minute:02}': v
                      for k, v in load.strategy.state.desired_energy.items()
                      }

    for timepoint, energy in desired_energy.items():
        if timepoint in input_profile:
            assert energy == input_profile[timepoint] / \
                   (Interval(hours=1) / load.config.slot_length)
        else:
            assert False


@then('load only accepted offers lower than max_energy_rate')
def check_traded_energy_rate(context):
    house = next(filter(lambda x: x.name == "House 1", context.simulation.area.children))
    load = next(filter(lambda x: "H1 DefinedLoad" in x.name, house.children))

    for slot, market in house.past_markets.items():
        for trade in market.trades:
            if trade.buyer == load.name:
                assert (trade.offer.price / trade.offer.energy) <\
                       load.strategy.max_energy_rate.m


@then('the DefinedLoadStrategy follows the Load profile provided as dict')
def check_user_pv_dict_profile(context):
    house = next(filter(lambda x: x.name == "House 1", context.simulation.area.children))
    load = next(filter(lambda x: x.name == "H1 DefinedLoad", house.children))
    from d3a.setup.strategy_tests.user_profile_load_dict import user_profile

    for slot, market in house.past_markets.items():
        if slot.hour in user_profile.keys():
            assert load.strategy.state.desired_energy[slot] == user_profile[slot.hour] / \
                   (Interval(hours=1) / house.config.slot_length)
        else:
            assert load.strategy.state.desired_energy[slot] == 0