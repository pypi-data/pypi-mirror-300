#
# Copyright 2017 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import warnings

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from . import performance as perf
from . import plotting
from . import utils
import empyrical as ep
from scipy import stats

class GridFigure(object):
    """
    It makes life easier with grid plots
    """

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.fig = plt.figure(figsize=(14, rows * 7))
        self.gs = gridspec.GridSpec(rows, cols, wspace=0.4, hspace=0.3)
        self.curr_row = 0
        self.curr_col = 0

    def next_row(self):
        if self.curr_col != 0:
            self.curr_row += 1
            self.curr_col = 0
        subplt = plt.subplot(self.gs[self.curr_row, :])
        self.curr_row += 1
        return subplt

    def next_cell(self):
        if self.curr_col >= self.cols:
            self.curr_row += 1
            self.curr_col = 0
        subplt = plt.subplot(self.gs[self.curr_row, self.curr_col])
        self.curr_col += 1
        return subplt

    def close(self):
        plt.close(self.fig)
        self.fig = None
        self.gs = None


@plotting.customize
def create_summary_tear_sheet(
        factor_data, long_short=True, group_neutral=False
):
    """
    Creates a small summary tear sheet with returns, information, and turnover
    analysis.

    Parameters
    ----------
    factor_data : pd.DataFrame - MultiIndex
        A MultiIndex DataFrame indexed by date (level 0) and asset (level 1),
        containing the values for a single alpha factor, forward returns for
        each period, the factor quantile/bin that factor value belongs to, and
        (optionally) the group the asset belongs to.
        - See full explanation in utils.get_clean_factor_and_forward_returns
    long_short : bool
        Should this computation happen on a long short portfolio? if so, then
        mean quantile returns will be demeaned across the factor universe.
    group_neutral : bool
        Should this computation happen on a group neutral portfolio? if so,
        returns demeaning will occur on the group level.
    """

    # Returns Analysis
    mean_quant_ret, std_quantile = perf.mean_return_by_quantile(
        factor_data,
        by_group=False,
        demeaned=long_short,
        group_adjust=group_neutral,
    )

    mean_quant_rateret = mean_quant_ret.apply(
        utils.rate_of_return, axis=0, base_period=mean_quant_ret.columns[0]
    )

    mean_quant_ret_bydate, std_quant_daily = perf.mean_return_by_quantile(
        factor_data,
        by_date=True,
        by_group=False,
        demeaned=long_short,
        group_adjust=group_neutral,
    )

    mean_quant_rateret_bydate = mean_quant_ret_bydate.apply(
        utils.rate_of_return,
        axis=0,
        base_period=mean_quant_ret_bydate.columns[0],
    )

    compstd_quant_daily = std_quant_daily.apply(
        utils.std_conversion, axis=0, base_period=std_quant_daily.columns[0]
    )

    alpha_beta = perf.factor_alpha_beta(
        factor_data, demeaned=long_short, group_adjust=group_neutral
    )

    mean_ret_spread_quant, std_spread_quant = perf.compute_mean_returns_spread(
        mean_quant_rateret_bydate,
        factor_data["factor_quantile"].max(),
        factor_data["factor_quantile"].min(),
        std_err=compstd_quant_daily,
    )

    periods = utils.get_forward_returns_columns(factor_data.columns)
    periods = list(map(lambda p: pd.Timedelta(p).days, periods))

    fr_cols = len(periods)
    vertical_sections = 2 + fr_cols * 3

    plotting.plot_quantile_statistics_table(factor_data)

    plotting.plot_returns_table(
        alpha_beta, mean_quant_rateret, mean_ret_spread_quant
    )

    plotting.plot_quantile_returns_bar(
        mean_quant_rateret,
        by_group=False,
        ylim_percentiles=None
    )

    # Information Analysis
    ic = perf.factor_information_coefficient(factor_data)
    plotting.plot_information_table(ic)

    # Turnover Analysis
    quantile_factor = factor_data["factor_quantile"]

    quantile_turnover = {
        p: pd.concat(
            [
                perf.quantile_turnover(quantile_factor, q, p)
                for q in range(1, int(quantile_factor.max()) + 1)
            ],
            axis=1,
        )
        for p in periods
    }

    autocorrelation = pd.concat(
        [
            perf.factor_rank_autocorrelation(factor_data, period)
            for period in periods
        ],
        axis=1,
    )

    plotting.plot_turnover_table(autocorrelation, quantile_turnover)

    plt.show()


@plotting.customize
def create_returns_tear_sheet(
        factor_data, long_short=True, group_neutral=False, by_group=False
):
    """
    Creates a tear sheet for returns analysis of a factor.

    Parameters
    ----------
    factor_data : pd.DataFrame - MultiIndex
        A MultiIndex DataFrame indexed by date (level 0) and asset (level 1),
        containing the values for a single alpha factor, forward returns for
        each period, the factor quantile/bin that factor value belongs to,
        and (optionally) the group the asset belongs to.
        - See full explanation in utils.get_clean_factor_and_forward_returns
    long_short : bool
        Should this computation happen on a long short portfolio? if so, then
        mean quantile returns will be demeaned across the factor universe.
        Additionally factor values will be demeaned across the factor universe
        when factor weighting the portfolio for cumulative returns plots
    group_neutral : bool
        Should this computation happen on a group neutral portfolio? if so,
        returns demeaning will occur on the group level.
        Additionally each group will weight the same in cumulative returns
        plots
    by_group : bool
        If True, display graphs separately for each group.
    """

    factor_returns = perf.factor_returns(
        factor_data, long_short, group_neutral
    )

    mean_quant_ret, std_quantile = perf.mean_return_by_quantile(
        factor_data,
        by_group=False,
        demeaned=long_short,
        group_adjust=group_neutral,
    )

    mean_quant_rateret = mean_quant_ret.apply(
        utils.rate_of_return, axis=0, base_period=mean_quant_ret.columns[0]
    )

    mean_quant_ret_bydate, std_quant_daily = perf.mean_return_by_quantile(
        factor_data,
        by_date=True,
        by_group=False,
        demeaned=long_short,
        group_adjust=group_neutral,
    )

    mean_quant_rateret_bydate = mean_quant_ret_bydate.apply(
        utils.rate_of_return,
        axis=0,
        base_period=mean_quant_ret_bydate.columns[0],
    )

    compstd_quant_daily = std_quant_daily.apply(
        utils.std_conversion, axis=0, base_period=std_quant_daily.columns[0]
    )

    alpha_beta = perf.factor_alpha_beta(
        factor_data, factor_returns, long_short, group_neutral
    )

    mean_ret_spread_quant, std_spread_quant = perf.compute_mean_returns_spread(
        mean_quant_rateret_bydate,
        factor_data["factor_quantile"].max(),
        factor_data["factor_quantile"].min(),
        std_err=compstd_quant_daily,
    )

    fr_cols = len(factor_returns.columns)
    vertical_sections = 2 + fr_cols * 3

    plotting.plot_returns_table(
        alpha_beta, mean_quant_rateret, mean_ret_spread_quant
    )

    plotting.plot_quantile_returns_bar(
        mean_quant_rateret,
        by_group=False,
        ylim_percentiles=None
    )

    plotting.plot_quantile_returns_violin(
        mean_quant_rateret_bydate, ylim_percentiles=(1, 99)
    )

    trading_calendar = factor_data.index.levels[0].freq
    if trading_calendar is None:
        trading_calendar = pd.tseries.offsets.BDay()
        warnings.warn(
            "'freq' not set in factor_data index: assuming business day",
            UserWarning,
        )

    # Compute cumulative returns from daily simple returns, if '1D'
    # returns are provided.
    if "1D" in factor_returns:
        title = (
            "Factor Weighted "
            + ("Group Neutral " if group_neutral else "")
            + ("Long/Short " if long_short else "")
            + "Portfolio Cumulative Return (1D Period)"
        )

        plotting.plot_cumulative_returns(
            factor_returns["1D"], period="1D", title=title
        )

        plotting.plot_cumulative_returns_by_quantile(
            mean_quant_ret_bydate["1D"], period="1D"
        )

    plotting.plot_mean_quantile_returns_spread_time_series(
        mean_ret_spread_quant,
        std_err=std_spread_quant,
        bandwidth=0.5
    )

    if by_group:
        (
            mean_return_quantile_group,
            mean_return_quantile_group_std_err,
        ) = perf.mean_return_by_quantile(
            factor_data,
            by_date=False,
            by_group=True,
            demeaned=long_short,
            group_adjust=group_neutral,
        )

        mean_quant_rateret_group = mean_return_quantile_group.apply(
            utils.rate_of_return,
            axis=0,
            base_period=mean_return_quantile_group.columns[0],
        )

        num_groups = len(
            mean_quant_rateret_group.index.get_level_values("group").unique()
        )

        vertical_sections = 1 + (((num_groups - 1) // 2) + 1)

        plotting.plot_quantile_returns_bar(
            mean_quant_rateret_group,
            by_group=True,
            ylim_percentiles=(5, 95)
        )


@plotting.customize
def create_information_tear_sheet(
        factor_data, group_neutral=False, by_group=False
):
    """
    Creates a tear sheet for information analysis of a factor.

    Parameters
    ----------
    factor_data : pd.DataFrame - MultiIndex
        A MultiIndex DataFrame indexed by date (level 0) and asset (level 1),
        containing the values for a single alpha factor, forward returns for
        each period, the factor quantile/bin that factor value belongs to, and
        (optionally) the group the asset belongs to.
        - See full explanation in utils.get_clean_factor_and_forward_returns
    group_neutral : bool
        Demean forward returns by group before computing IC.
    by_group : bool
        If True, display graphs separately for each group.
    """

    ic = perf.factor_information_coefficient(factor_data, group_neutral)

    plotting.plot_information_table(ic)

    columns_wide = 2
    fr_cols = len(ic.columns)
    rows_when_wide = ((fr_cols - 1) // columns_wide) + 1
    vertical_sections = fr_cols + 3 * rows_when_wide + 2 * fr_cols

    plotting.plot_ic_ts(ic)

    plotting.plot_ic_hist(ic)
    plotting.plot_ic_qq(ic)

    if not by_group:
        mean_monthly_ic = perf.mean_information_coefficient(
            factor_data,
            group_adjust=group_neutral,
            by_group=False,
            by_time="M",
        )
        plotting.plot_monthly_ic_heatmap(
            mean_monthly_ic
        )

    if by_group:
        mean_group_ic = perf.mean_information_coefficient(
            factor_data, group_adjust=group_neutral, by_group=True
        )

        plotting.plot_ic_by_group(mean_group_ic)


@plotting.customize
def create_turnover_tear_sheet(factor_data, turnover_periods=None):
    """
    Creates a tear sheet for analyzing the turnover properties of a factor.

    Parameters
    ----------
    factor_data : pd.DataFrame - MultiIndex
        A MultiIndex DataFrame indexed by date (level 0) and asset (level 1),
        containing the values for a single alpha factor, forward returns for
        each period, the factor quantile/bin that factor value belongs to, and
        (optionally) the group the asset belongs to.
        - See full explanation in utils.get_clean_factor_and_forward_returns
    turnover_periods : sequence[string], optional
        Periods to compute turnover analysis on. By default periods in
        'factor_data' are used but custom periods can provided instead. This
        can be useful when periods in 'factor_data' are not multiples of the
        frequency at which factor values are computed i.e. the periods
        are 2h and 4h and the factor is computed daily and so values like
        ['1D', '2D'] could be used instead
    """

    if turnover_periods is None:
        input_periods = utils.get_forward_returns_columns(
            factor_data.columns, require_exact_day_multiple=True,
        ).to_numpy()
        turnover_periods = utils.timedelta_strings_to_integers(input_periods)
    else:
        turnover_periods = utils.timedelta_strings_to_integers(
            turnover_periods,
        )

    quantile_factor = factor_data["factor_quantile"]

    quantile_turnover = {
        p: pd.concat(
            [
                perf.quantile_turnover(quantile_factor, q, p)
                for q in quantile_factor.sort_values().unique().tolist()
            ],
            axis=1,
        )
        for p in turnover_periods
    }

    autocorrelation = pd.concat(
        [
            perf.factor_rank_autocorrelation(factor_data, period)
            for period in turnover_periods
        ],
        axis=1,
    )

    plotting.plot_turnover_table(autocorrelation, quantile_turnover)

    fr_cols = len(turnover_periods)
    columns_wide = 1
    rows_when_wide = ((fr_cols - 1) // 1) + 1
    vertical_sections = fr_cols + 3 * rows_when_wide + 2 * fr_cols

    for period in turnover_periods:
        if quantile_turnover[period].isnull().all().all():
            continue
        plotting.plot_top_bottom_quantile_turnover(
            quantile_turnover[period], period=period
        )

    for period in autocorrelation:
        if autocorrelation[period].isnull().all():
            continue
        plotting.plot_factor_rank_auto_correlation(
            autocorrelation[period], period=period
        )


@plotting.customize
def create_full_tear_sheet(factor_data,
                           long_short=True,
                           group_neutral=False,
                           by_group=False):
    """
    Creates a full tear sheet for analysis and evaluating single
    return predicting (alpha) factor.

    Parameters
    ----------
    factor_data : pd.DataFrame - MultiIndex
        A MultiIndex DataFrame indexed by date (level 0) and asset (level 1),
        containing the values for a single alpha factor, forward returns for
        each period, the factor quantile/bin that factor value belongs to, and
        (optionally) the group the asset belongs to.
        - See full explanation in utils.get_clean_factor_and_forward_returns
    long_short : bool
        Should this computation happen on a long short portfolio?
        - See tears.create_returns_tear_sheet for details on how this flag
        affects returns analysis
    group_neutral : bool
        Should this computation happen on a group neutral portfolio?
        - See tears.create_returns_tear_sheet for details on how this flag
        affects returns analysis
        - See tears.create_information_tear_sheet for details on how this
        flag affects information analysis
    by_group : bool
        If True, display graphs separately for each group.
    """

    plotting.plot_quantile_statistics_table(factor_data)
    create_returns_tear_sheet(
        factor_data, long_short, group_neutral, by_group, set_context=False
    )
    create_information_tear_sheet(
        factor_data, group_neutral, by_group, set_context=False
    )
    create_turnover_tear_sheet(factor_data, set_context=False)
    plotting.plt.show()


@plotting.customize
def create_event_returns_tear_sheet(factor_data,
                                    returns,
                                    avgretplot=(5, 15),
                                    long_short=True,
                                    group_neutral=False,
                                    std_bar=True,
                                    by_group=False):
    """
    Creates a tear sheet to view the average cumulative returns for a
    factor within a window (pre and post event).

    Parameters
    ----------
    factor_data : pd.DataFrame - MultiIndex
        A MultiIndex Series indexed by date (level 0) and asset (level 1),
        containing the values for a single alpha factor, the factor
        quantile/bin that factor value belongs to and (optionally) the group
        the asset belongs to.
        - See full explanation in utils.get_clean_factor_and_forward_returns
    returns : pd.DataFrame
        A DataFrame indexed by date with assets in the columns containing daily
        returns.
        - See full explanation in utils.get_clean_factor_and_forward_returns
    avgretplot: tuple (int, int) - (before, after)
        If not None, plot quantile average cumulative returns
    long_short : bool
        Should this computation happen on a long short portfolio? if so then
        factor returns will be demeaned across the factor universe
    group_neutral : bool
        Should this computation happen on a group neutral portfolio? if so,
        returns demeaning will occur on the group level.
    std_bar : boolean, optional
        Show plots with standard deviation bars, one for each quantile
    by_group : bool
        If True, display graphs separately for each group.
    """

    before, after = avgretplot

    avg_cumulative_returns = perf.average_cumulative_return_by_quantile(
        factor_data,
        returns,
        periods_before=before,
        periods_after=after,
        demeaned=long_short,
        group_adjust=group_neutral,
    )

    num_quantiles = int(factor_data["factor_quantile"].max())

    vertical_sections = 1
    if std_bar:
        vertical_sections += ((num_quantiles - 1) // 2) + 1
    cols = 2 if num_quantiles != 1 else 1
    plotting.plot_quantile_average_cumulative_return(
        avg_cumulative_returns,
        by_quantile=False,
        std_bar=False
    )
    if std_bar:
        plotting.plot_quantile_average_cumulative_return(
            avg_cumulative_returns,
            by_quantile=True,
            std_bar=True
        )

    plt.show()

    if by_group:
        groups = factor_data["group"].unique()
        num_groups = len(groups)
        vertical_sections = ((num_groups - 1) // 2) + 1

        avg_cumret_by_group = perf.average_cumulative_return_by_quantile(
            factor_data,
            returns,
            periods_before=before,
            periods_after=after,
            demeaned=long_short,
            group_adjust=group_neutral,
            by_group=True,
        )

        for group, avg_cumret in avg_cumret_by_group.groupby(level="group"):
            avg_cumret.index = avg_cumret.index.droplevel("group")
            plotting.plot_quantile_average_cumulative_return(
                avg_cumret,
                by_quantile=False,
                std_bar=False,
                title=group
            )

        plt.show()


@plotting.customize
def create_event_study_tear_sheet(factor_data,
                                  returns,
                                  avgretplot=(5, 15),
                                  rate_of_ret=True,
                                  n_bars=50):
    """
    Creates an event study tear sheet for analysis of a specific event.

    Parameters
    ----------
    factor_data : pd.DataFrame - MultiIndex
        A MultiIndex DataFrame indexed by date (level 0) and asset (level 1),
        containing the values for a single event, forward returns for each
        period, the factor quantile/bin that factor value belongs to, and
        (optionally) the group the asset belongs to.
    returns : pd.DataFrame, required only if 'avgretplot' is provided
        A DataFrame indexed by date with assets in the columns containing daily
        returns.
        - See full explanation in utils.get_clean_factor_and_forward_returns
    avgretplot: tuple (int, int) - (before, after), optional
        If not None, plot event style average cumulative returns within a
        window (pre and post event).
    rate_of_ret : bool, optional
        Display rate of return instead of simple return in 'Mean Period Wise
        Return By Factor Quantile' and 'Period Wise Return By Factor Quantile'
        plots
    n_bars : int, optional
        Number of bars in event distribution plot
    """

    long_short = False

    plotting.plot_quantile_statistics_table(factor_data)

    plotting.plot_events_distribution(
        events=factor_data["factor"], num_bars=n_bars
    )
    plt.show()

    if returns is not None and avgretplot is not None:
        create_event_returns_tear_sheet(
            factor_data=factor_data,
            returns=returns,
            avgretplot=avgretplot,
            long_short=long_short,
            group_neutral=False,
            std_bar=True,
            by_group=False,
        )

    factor_returns = perf.factor_returns(
        factor_data, demeaned=False, equal_weight=True
    )

    mean_quant_ret, std_quantile = perf.mean_return_by_quantile(
        factor_data, by_group=False, demeaned=long_short
    )
    if rate_of_ret:
        mean_quant_ret = mean_quant_ret.apply(
            utils.rate_of_return, axis=0, base_period=mean_quant_ret.columns[0]
        )

    mean_quant_ret_bydate, std_quant_daily = perf.mean_return_by_quantile(
        factor_data, by_date=True, by_group=False, demeaned=long_short
    )
    if rate_of_ret:
        mean_quant_ret_bydate = mean_quant_ret_bydate.apply(
            utils.rate_of_return,
            axis=0,
            base_period=mean_quant_ret_bydate.columns[0],
        )

    fr_cols = len(factor_returns.columns)
    vertical_sections = 2 + fr_cols * 1

    plotting.plot_quantile_returns_bar(
        mean_quant_ret, by_group=False, ylim_percentiles=None
    )

    plotting.plot_quantile_returns_violin(
        mean_quant_ret_bydate, ylim_percentiles=(1, 99)
    )

    trading_calendar = factor_data.index.levels[0].freq
    if trading_calendar is None:
        trading_calendar = pd.tseries.offsets.BDay()
        warnings.warn(
            "'freq' not set in factor_data index: assuming business day",
            UserWarning,
        )

    plt.show()

################################################################################


def sd_plot_factor_statistics_table(factor_data):
    plotting.sd_plot_quantile_statistics_table(factor_data)


def sd_get_return_results(factor_data, turnover_Data, ana_mode, plot):
    if ana_mode == 'longonly' or ana_mode == 'benchmark':
        longshort = False
    elif ana_mode == 'longshort':
        longshort = True

    input_periods = utils.get_forward_returns_columns(
        factor_data.columns, require_exact_day_multiple=True,).to_numpy()
    input_periods = np.array(
        utils.timedelta_strings_to_integers(input_periods))

    top_quant = factor_data["factor_quantile"].max()
    bottom_quant = factor_data["factor_quantile"].min()

    if turnover_Data is None:
        turnover_Data = sd_get_turnover_result(factor_data, False)
    quantile_turnover = turnover_Data['quantile_turnover']

    # 分位数分组每日收益
    mean_quant_ret_bydate, std_quant_daily = perf.mean_return_by_quantile(
        factor_data,
        by_date=True,
        by_group=False,
        demeaned=longshort,
        group_adjust=False,
    )
    # 统一为日收益
    mean_quant_rateret_bydate = mean_quant_ret_bydate.apply(
        utils.rate_of_return,
        axis=0,
        base_period=mean_quant_ret_bydate.columns[0],
    )

    # 换手手续费
    expenses = quantile_turnover * -0.0013
    expenses_bydate = expenses.swaplevel(0, 1).reindex(
        mean_quant_rateret_bydate.index).fillna(0)
    mean_quant_rateret_bydate_ae = mean_quant_rateret_bydate + expenses_bydate
    # mean_quant_ret_bydate_ae = mean_quant_ret_bydate + expenses_bydate

    # # 统一为日标准差
    # compstd_quant_daily = std_quant_daily.apply(
    #     utils.std_conversion, axis=0, base_period=std_quant_daily.columns[0]
    # )

    # 计算首尾分组收益差(即多空收益)
    mean_ret_spread_quant, std_spread_quant = perf.compute_mean_returns_spread(
        mean_quant_rateret_bydate,
        top_quant,
        bottom_quant,
        # std_err=compstd_quant_daily,
    )

    mean_ret_spread_quant_ae = expenses.xs(top_quant, level='factor_quantile') + \
        expenses.xs(bottom_quant, level='factor_quantile')

    mean_ret_spread_quant_ae = mean_ret_spread_quant + \
        mean_ret_spread_quant_ae.reindex(mean_ret_spread_quant.index).fillna(0)

    # 因子看板用
    ret_wide = mean_quant_rateret_bydate["1D"].unstack('factor_quantile')
    ret_wide_ae = mean_quant_rateret_bydate_ae["1D"].unstack('factor_quantile')
    cum_ret = ret_wide.apply(perf.cumulative_returns)
    cum_ret_ae = ret_wide_ae.apply(perf.cumulative_returns)

    # 计算年化收益
    days = len(ret_wide)

    if ana_mode == 'longonly':
        mean_quant_rateret = (mean_quant_rateret_bydate.add(1).groupby(mean_quant_rateret_bydate.index.get_level_values('factor_quantile'))
                              .apply('prod')**(243/days)).add(-1)
        mean_quant_rateret_ae = (mean_quant_rateret_bydate_ae.add(1).groupby(mean_quant_rateret_bydate.index.get_level_values('factor_quantile'))
                                 .apply('prod')**(243/days)).add(-1)
    else:
        mean_quant_rateret = (mean_quant_rateret_bydate.groupby(mean_quant_rateret_bydate.index.get_level_values('factor_quantile'))
                              .apply('mean')*(243))
        mean_quant_rateret_ae = (mean_quant_rateret_bydate_ae.groupby(mean_quant_rateret_bydate_ae.index.get_level_values('factor_quantile'))
                                 .apply('mean')*(243))

    # 分组收益表格
    returns_table = pd.DataFrame(columns=mean_quant_ret_bydate.columns)
    returns_table.loc["Annualized Return Top Quantile (%)"] = mean_quant_rateret.loc[top_quant]*100
    returns_table.loc["Annualized Return Bottom Quantile (%)"] = mean_quant_rateret.loc[bottom_quant]*100
    returns_table.loc["Annualized ReturnAE Top Quantile (%)"] = mean_quant_rateret_ae.loc[top_quant]*100
    returns_table.loc["Annualized ReturnAE Bottom Quantile (%)"] = mean_quant_rateret_ae.loc[bottom_quant]*100

    if ana_mode == 'longshort':
        returns_table.loc["Annualized Spread ReturnAE(%)"] = \
            mean_ret_spread_quant_ae.mean() * 100 * 243
        returns_table.loc["Spread ReturnAE max_drawdown(%)"] = \
            ep.max_drawdown(mean_ret_spread_quant_ae).values*100
        returns_table.loc["Spread ReturnAE SharpeRatio"] = \
            ep.sharpe_ratio(mean_ret_spread_quant_ae)/(input_periods**0.5)
    else:
        returns_table.loc["ReturnAE Top Quantile max_drawdown(%)"] = ep.max_drawdown(mean_quant_rateret_bydate_ae.xs(
            top_quant, level='factor_quantile')).values*100
        returns_table.loc["ReturnAE Top Quantile SharpeRatio"] = ep.sharpe_ratio(mean_quant_rateret_bydate_ae.xs(
            top_quant, level='factor_quantile'))/(input_periods**0.5)

    # 分年处理
    returns_table_byYear = pd.DataFrame()
    # 年化收益
    if ana_mode == 'longonly':
        mean_quant_rateret_byYear = (ret_wide.add(1).groupby(ret_wide.index.get_level_values('date').to_period('A')).apply('prod')**(
            243/ret_wide.add(1).groupby(ret_wide.index.get_level_values('date').to_period('A')).apply('count'))).add(-1)
        mean_quant_rateret_byYear_ae = (ret_wide_ae.add(1).groupby(ret_wide_ae.index.get_level_values('date').to_period('A')).apply('prod')**(
            243/ret_wide_ae.add(1).groupby(ret_wide_ae.index.get_level_values('date').to_period('A')).apply('count'))).add(-1)
    else:
        mean_quant_rateret_byYear = ret_wide.groupby(ret_wide.index.get_level_values('date').to_period('A')).apply('mean')*243
        mean_quant_rateret_byYear_ae = ret_wide_ae.groupby(ret_wide_ae.index.get_level_values('date').to_period('A')).apply('mean')*243

    mean_ret_spread_quan_byYeart = mean_ret_spread_quant['1D'].groupby(mean_ret_spread_quant['1D'].index.get_level_values('date').to_period('A')).apply('mean')*243
    mean_ret_spread_quan_byYeart_ae = mean_ret_spread_quant_ae['1D'].groupby(mean_ret_spread_quant_ae['1D'].index.get_level_values('date').to_period('A')).apply('mean')*243

    returns_table_byYear["Annualized Return Top Quantile (%)"] = mean_quant_rateret_byYear[top_quant] * 100
    returns_table_byYear["Annualized ReturnAE Top Quantile (%)"] = mean_quant_rateret_byYear_ae[top_quant] * 100
    returns_table_byYear["Annualized Return Bottom Quantile (%)"] = mean_quant_rateret_byYear[bottom_quant] * 100
    returns_table_byYear["Annualized ReturnAE Bottom Quantile (%)"] = mean_quant_rateret_byYear_ae[bottom_quant] * 100
    returns_table_byYear["Annualized Spread Return(%)"] = mean_ret_spread_quan_byYeart * 100
    returns_table_byYear["Annualized Spread ReturnAE(%)"] = mean_ret_spread_quan_byYeart_ae * 100

    if ana_mode == 'longshort':
        returns_table_byYear["Spread ReturnAE SharpeRatio"] = mean_ret_spread_quant_ae['1D'].groupby(mean_ret_spread_quant_ae['1D'].index.get_level_values('date').to_period('A')).apply(ep.sharpe_ratio)
        returns_table_byYear["Spread ReturnAE max_drawdown"] = mean_ret_spread_quant_ae['1D'].groupby(mean_ret_spread_quant_ae['1D'].index.get_level_values('date').to_period('A')).apply(ep.max_drawdown) * 100

    top_quant_data = mean_quant_rateret_bydate_ae['1D'].xs(top_quant, level='factor_quantile')
    returns_table_byYear["ReturnAE Top Quantile SharpeRatio"] = \
        top_quant_data.groupby(top_quant_data.index.get_level_values('date').to_period('A')).apply(ep.sharpe_ratio)
    returns_table_byYear["ReturnAE Top Quantile max_drawdown(%)"] = \
        top_quant_data.groupby(top_quant_data.index.get_level_values('date').to_period('A')).apply(ep.max_drawdown) * 100

    if plot:
        # 输出分组收益表格

        title = (ana_mode + " AnalysisMode " + "Returns Analysis ")
        print(title)
        utils.print_table(returns_table.apply(lambda x: x.round(2)))
        print("\n")

        # 画分组收益图
        plotting.sd_plot_quantile_returns_bar(
            mean_quant_rateret,
            by_group=False,
            ylim_percentiles=None
        )
        # 画分组累计收益图
        if ana_mode == 'benchmark':
            if "1D" in mean_quant_rateret_bydate:
                plotting.sd_plot_cumulative_excessreturn_by_quantile(
                    mean_quant_rateret_bydate["1D"], period="1D"
                )
                plotting.sd_plot_cumulative_excessreturn(
                    pd.concat([mean_quant_rateret_bydate["1D"].xs(
                        top_quant, level='factor_quantile'),
                        mean_quant_rateret_bydate_ae["1D"].xs(
                            top_quant, level='factor_quantile')], axis=1), period="1D"
                )
        else:
            if "1D" in mean_quant_rateret_bydate:
                plotting.sd_plot_cumulative_returns_by_quantile(
                    mean_quant_rateret_bydate["1D"], period="1D", longshort=longshort
                )
            if "1D" in mean_ret_spread_quant:
                plotting.sd_plot_cumulative_returns_spread(
                    pd.concat([mean_ret_spread_quant["1D"], mean_ret_spread_quant_ae["1D"]], axis=1), period="1D"
                )
        # 输出分年收益表格
        title = (ana_mode + " AnalysisMode " + "Returns Analysis By Year ")
        print(title)
        utils.print_table(returns_table_byYear.apply(lambda x: x.round(2)))
        print("\n")

    ret_Data = {}
    ret_Data['returns_table'] = returns_table
    ret_Data['ret_quant_daily'] = mean_quant_rateret_bydate
    ret_Data['ret_spread_quant_daily'] = mean_ret_spread_quant
    ret_Data['ret_quant_daily_ae'] = mean_quant_rateret_bydate_ae
    ret_Data['ret_spread_quant_daily_ae'] = mean_ret_spread_quant_ae
    ret_Data['cum_ret'] = cum_ret
    ret_Data['ret_wide'] = ret_wide
    ret_Data['cum_ret_ae'] = cum_ret_ae
    ret_Data['ret_wide_ae'] = ret_wide_ae
    ret_Data['returns_table_byYear'] = returns_table_byYear

    ret_Data['quantile_return'] = mean_quant_rateret
    ret_Data['quantile_return_ae'] = mean_quant_rateret_ae

    return ret_Data


def sd_get_information_result(factor_data, plot):
    ic_data = perf.factor_information_coefficient(factor_data, False)
    ic_data_sd_20D = sd_factor_information_coefficient(factor_data, 20)
    ic_data_sd_60D = sd_factor_information_coefficient(factor_data, 60)

    ic_summary_table = pd.DataFrame()
    ic_summary_table["IC Mean"] = ic_data.mean()
    #ic_summary_table["IC Std."] = ic_data.std()
    ic_summary_table["IR"] = \
        ic_data.mean() / ic_data.std()
    ic_summary_table["Good IC Ratio"] = len(ic_data[abs(ic_data['1D']) > 0.02])/len(ic_data)

    ic_summary_table["IC Mean SD_20D"] = ic_data_sd_20D.mean()
    #ic_summary_table["IC Std SD_20D"] = ic_data_sd_20D.std()
    ic_summary_table["IR SD_20D"] = \
        ic_data_sd_20D.mean() / ic_data_sd_20D.std()

    ic_summary_table["IC Mean SD_60D"] = ic_data_sd_60D.mean()
   # ic_summary_table["IC Std SD_60D"] = ic_data_sd_60D.std()
    ic_summary_table["IR SD_60D"] = \
        ic_data_sd_60D.mean() / ic_data_sd_60D.std()
    if plot:
        print("Information Analysis")
        utils.print_table(ic_summary_table.apply(lambda x: x.round(3)).T)
        print("\n")
        # plotting.plot_ic_ts(ic_data)
    return ic_summary_table


def sd_factor_information_coefficient(factor_data, window):
    def src_ic(group):
        f = group['factor_quantile']
        _ic = group[utils.get_forward_returns_columns(factor_data.columns)] \
            .apply(lambda x: stats.spearmanr(x, f)[0])
        return _ic

    def sum_rtn(group):
        group[utils.get_forward_returns_columns(factor_data.columns)] = group[utils.get_forward_returns_columns(
            factor_data.columns)].rolling(window).sum()
        return group

    factor_data = factor_data.copy()
    mean_quant_ret = factor_data.groupby(['date', 'factor_quantile'])[
        utils.get_forward_returns_columns(factor_data.columns)].mean().reset_index()
    mean_quant_ret_window = mean_quant_ret.groupby(
        ['factor_quantile']).apply(sum_rtn).reset_index()

    ic = mean_quant_ret_window.groupby('date').apply(src_ic)

    return ic


def sd_get_turnover_result(factor_data, plot):
    input_periods = utils.get_forward_returns_columns(
        factor_data.columns, require_exact_day_multiple=True,
    ).to_numpy()
    turnover_periods = utils.timedelta_strings_to_integers(input_periods)

    quantile_factor = factor_data["factor_quantile"]

    quantile_turnover = {
        p: pd.concat(
            [
                perf.quantile_turnover(quantile_factor, q, p)
                for q in quantile_factor.sort_values().unique().tolist()
            ],
            axis=1,
        )
        for p in turnover_periods
    }

    autocorrelation = pd.concat(
        [
            perf.factor_rank_autocorrelation(factor_data, period)
            for period in turnover_periods
        ],
        axis=1,
    )

    turnover_table = pd.DataFrame()
    for period in sorted(quantile_turnover.keys()):
        for quantile, p_data in quantile_turnover[period].iteritems():
            turnover_table.loc["Quantile {} Mean Turnover".format(quantile),
                               "{}D".format(period)] = p_data.mean()/period
    auto_corr = pd.DataFrame()
    for period, p_data in autocorrelation.iteritems():
        auto_corr.loc["Mean Factor Rank Autocorrelation",
                      "{}D".format(period)] = p_data.mean()
    if plot:
        print("Turnover Analysis")
        utils.print_table(turnover_table.apply(lambda x: x.round(3)))
        print("\n")
        utils.print_table(auto_corr.apply(lambda x: x.round(3)))
        print("\n")

        for period in turnover_periods:
            if quantile_turnover[period].isnull().all().all():
                continue
            plotting.plot_top_bottom_quantile_turnover(
                quantile_turnover[period], period=period
            )

        for period in autocorrelation:
            if autocorrelation[period].isnull().all():
                continue
            plotting.plot_factor_rank_auto_correlation(
                autocorrelation[period], period=period
            )
    quantile_turnover_temp = pd.DataFrame()
    for t in range(len(turnover_periods)):
        quantile_turnover_temp[input_periods[t]] = quantile_turnover[turnover_periods[t]].stack(
        )/turnover_periods[t]
    quantile_turnover_temp.index.set_names(
        ['date', 'factor_quantile'], inplace=True)

    turnover_Data = {}
    turnover_Data['turnover_table'] = turnover_table

    turnover_Data['quantile_turnover'] = quantile_turnover_temp.fillna(0)
    return turnover_Data


@plotting.customize
def sd_get_Analysis_results(factor_data, ana_mode='longshort', plot=False):
    """
    自定义输出分析结果
    参数：
    ana_mode：longshort测试多空模式, longonly测试long-only模式,benchmark测试对标超额收益模式
    plot：True输出图像

    输出:Dict results,包括关键结果、收益率相关表、换手信息表格、IC值信息表格
    相关子表见后
    results['keyResuls_table']
    results['ret_Data'] = ret_Data
    results['turnover_Data'] = turnover_Data
    results['IC_Data'] = IC_Data

    可用函数包含:

    因子值统计
    tears.sd_plot_factor_statistics_table(factor_data)

    分组收益计算
    tears.sd_get_return_results(factor_data, turnover_Data, ana_mode, plot):
    参数：longshort=True多空模式,False做多模式
    参数：plot=True画图，False不画
    可选参数：turnover_Data换手信息，若不填或为none自动计算
    输出：
    ret_Data['returns_table']收益率结果
    ret_Data['returns_table_byYear']收益率结果按年统计
    ret_Data['ret_quant_daily']分组日收益
    ret_Data['ret_spread_quant_daily']多空收益
    ret_Data['ret_quant_daily_AE']费后分组日收益
    ret_Data['ret_spread_quant_daily_AE']费后多空收益
    ret_Data['cum_ret'] 累计分组收益
    ret_Data['ret_wide'] 分组日收益
    ret_Data['cum_ret_ae'] 累计费后分组收益
    ret_Data['ret_wide_ae'] 费后分组日收益
    ret_Data['quantile_return'] 分组年化收益
    ret_Data['quantile_return_ae'] 费后分组年化收益


    IC值计算
    tears.sd_get_information_result(factor_data,plot=True)
    参数：plot=True画图，False不画
    输出：IC值信息表格 IC_table

    换手计算
    tears.sd_get_turnover_result(factor_data,plot=True)
    参数：plot=True画图，False不画
    输出：换手信息表格，分组日换手
    turnover_Data['turnover_table']
    turnover_Data['quantile_turnover']


    """
    if ana_mode not in ['longonly', 'longshort', 'benchmark']:
        raise ValueError("ana_mode指定错误")

    # 因子值统计板块
    if plot:
        sd_plot_factor_statistics_table(factor_data)

    # 换手分析
    turnover_Data = sd_get_turnover_result(factor_data, plot=plot)

    # 收益分析板块
    # longshort为True时longshort模式分组统计，False时longonly模式
    ret_Data = sd_get_return_results(
        factor_data, turnover_Data=turnover_Data, ana_mode=ana_mode, plot=plot)

    # IC值
    IC_Data = sd_get_information_result(factor_data, plot=plot)

    keyResults_table = pd.DataFrame(columns=ret_Data['returns_table'].columns)
    if ana_mode == 'longshort':
        keyResults_table.loc['Annualized Spread ReturnAE(%)'] = ret_Data['returns_table'].loc[
            "Annualized Spread ReturnAE(%)"]
        keyResults_table.loc['Spread ReturnAE max_drawdown(%)'] = ret_Data[
            'returns_table'].loc["Spread ReturnAE max_drawdown(%)"]
        keyResults_table.loc['Spread ReturnAE SharpeRatio'] = ret_Data['returns_table'].loc["Spread ReturnAE SharpeRatio"]
    elif ana_mode == 'longonly' or ana_mode == 'benchmark':
        keyResults_table.loc['Annualized ReturnAE Top Quantile (%)'] = ret_Data['returns_table'].loc[
            "Annualized ReturnAE Top Quantile (%)"]
        keyResults_table.loc['ReturnAE Top Quantile max_drawdown(%)'] = ret_Data['returns_table'].loc[
            "ReturnAE Top Quantile max_drawdown(%)"]
        keyResults_table.loc['ReturnAE Top Quantile SharpeRatio'] = ret_Data['returns_table'].loc[
            "ReturnAE Top Quantile SharpeRatio"]

    keyResults_table.loc['IC_20'] = IC_Data['IC Mean SD_20D'].T
    keyResults_table.loc['IR_20'] = IC_Data['IR SD_20D'].T
    keyResults_table.loc['IC_60'] = IC_Data['IC Mean SD_60D'].T
    keyResults_table.loc['IR_60'] = IC_Data['IR SD_60D'].T

    keyResults_table.loc['Annualized ReturnAE Top Quantile (%)'] = ret_Data[
        'returns_table'].loc["Annualized ReturnAE Top Quantile (%)"]
    keyResults_table.loc['Annualized ReturnAE Bottom Quantile (%)'] = ret_Data[
        'returns_table'].loc["Annualized ReturnAE Bottom Quantile (%)"]
    keyResults_table.loc['Mean turnover Top Quantile'] = turnover_Data['turnover_table'].iloc[0]
    keyResults_table.loc['Mean turnover Bottom Quantile'] = turnover_Data['turnover_table'].iloc[-1]
    # turnover_Data['turnover_table'].iloc[0]

    results = {}
    results['keyResults'] = keyResults_table
    results['ret_Data'] = ret_Data
    results['turnover_Data'] = turnover_Data
    results['IC_Data'] = IC_Data

    return results
