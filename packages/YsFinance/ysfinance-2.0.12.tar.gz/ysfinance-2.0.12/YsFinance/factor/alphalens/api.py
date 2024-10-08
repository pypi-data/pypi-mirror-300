from . import tears

def create_summary_tear_sheet(
        factor_data, long_short=True, group_neutral=False
):
    return tears.create_summary_tear_sheet(
        factor_data, long_short, group_neutral)

def create_information_tear_sheet(
        factor_data, group_neutral=False, by_group=False
):
    return tears.create_information_tear_sheet(
        factor_data, group_neutral, by_group)

def create_turnover_tear_sheet(factor_data, turnover_periods=None):
    return tears.create_turnover_tear_sheet(factor_data, turnover_periods)


def create_full_tear_sheet(factor_data,
                           long_short=True,
                           group_neutral=False,
                           by_group=False):
    return tears.create_full_tear_sheet(factor_data,
                           long_short,
                           group_neutral,
                           by_group)

def create_event_returns_tear_sheet(factor_data,
                                    returns,
                                    avgretplot=(5, 15),
                                    long_short=True,
                                    group_neutral=False,
                                    std_bar=True,
                                    by_group=False):
    return tears.create_event_returns_tear_sheet(factor_data,
                                    returns,
                                    avgretplot,
                                    long_short,
                                    group_neutral,
                                    std_bar,
                                    by_group)

def create_event_study_tear_sheet(factor_data,
                                  returns,
                                  avgretplot=(5, 15),
                                  rate_of_ret=True,
                                  n_bars=50):
    return tears.create_event_study_tear_sheet(factor_data,
                                  returns,
                                  avgretplot,
                                  rate_of_ret,
                                  n_bars)

def sd_plot_factor_statistics_table(factor_data):
    return tears.sd_plot_factor_statistics_table(factor_data)


def sd_get_return_results(factor_data, turnover_Data, ana_mode, plot):
    return tears.sd_get_return_results(factor_data, turnover_Data, ana_mode, plot)


def sd_get_information_result(factor_data, plot):
    return tears.sd_get_information_result(factor_data, plot)


def sd_factor_information_coefficient(factor_data, window):
    return tears.sd_factor_information_coefficient(factor_data, window)

def sd_get_turnover_result(factor_data, plot):
    return tears.sd_get_turnover_result(factor_data, plot)


def sd_get_Analysis_results(factor_data, ana_mode='longshort', plot=False):
    return tears.sd_get_Analysis_results(factor_data, ana_mode, plot)


__all__ = []
__all__.extend(['create_summary_tear_sheet','create_information_tear_sheet','create_turnover_tear_sheet','create_full_tear_sheet',
                'create_event_returns_tear_sheet','create_event_study_tear_sheet','sd_plot_factor_statistics_table','sd_get_return_results',
                'sd_get_information_result','sd_factor_information_coefficient','sd_get_turnover_result','sd_get_Analysis_results'])