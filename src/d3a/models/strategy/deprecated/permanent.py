from d3a.d3a_core.exceptions import MarketException
from d3a.models.strategy import BaseStrategy
from d3a.models.state import LoadState


class PermanentLoadStrategy(BaseStrategy):
    parameters = ('energy', 'pre_buy_range')

    def __init__(self, energy=100, pre_buy_range=4):
        if energy <= 0 or pre_buy_range <= 1:
            raise ValueError("Incorrect parameter values for PermanentLoad.")
        super().__init__()
        self.energy = energy
        self.pre_buy_range = pre_buy_range
        self.state = LoadState()
        self.bought_in_market = set()

    def event_tick(self, *, area):
        try:
            for i, market in enumerate(area.all_markets):
                if i + 1 > self.pre_buy_range:
                    break
                if market in self.bought_in_market:
                    continue
                for offer in market.sorted_offers:
                    if offer.energy < self.energy / 1000:
                        continue
                    try:
                        self.accept_offer(market, offer)
                        self.bought_in_market.add(market)
                        break
                    except MarketException:
                        # Offer already gone etc., use next one.
                        continue
        except IndexError:
            pass

    def _update_energy_requirement(self):
        self.state.desired_energy_Wh[self.area.next_market.time_slot] = self.energy

    def event_market_cycle(self):
        self._update_energy_requirement()