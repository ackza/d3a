Feature: Storage tests

  Scenario: Storage break even range profile
     Given we have a scenario named strategy_tests/storage_strategy_break_even_range
     And d3a is installed
     When we run the d3a simulation with strategy_tests.storage_strategy_break_even_range [24, 15, 15]
     Then the storage devices buy and sell energy respecting the break even prices

  Scenario: Storage break even hourly profile
     Given we have a scenario named strategy_tests/storage_strategy_break_even_hourly
     And d3a is installed
     When we run the d3a simulation with strategy_tests.storage_strategy_break_even_hourly [24, 15, 15]
     Then the storage devices buy and sell energy respecting the hourly break even prices
