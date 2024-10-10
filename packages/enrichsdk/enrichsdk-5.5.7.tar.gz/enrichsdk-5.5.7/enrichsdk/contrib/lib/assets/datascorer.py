import pandas as pd

class BaseDataScorer(object):
    """
    Class to process data and produce some usable output
    This class is generic enough to handle arbitrary pandas dataframes
    """

    def __init__(self):
        """
        init the class
        """
        return

    ##
    ## internal methods
    ##

    def _spec_filter(self, df_orig, filters):
        """
        Apply a set of filters to a form5500 features dataframe
        """

        steps = []
        df = df_orig.copy()

        for fltr in filters:

            name = fltr.get("name", "")

            # get the params needed
            col = fltr.get("column")
            op = fltr.get("op")
            val = fltr.get("value")

            # check for correctness
            if (col is None) or (op is None) or (val is None):
                continue

            # perform the operation
            if op == "between":
                if len(val) != 2:
                    continue
                df = df[(df[col]>=val[0]) & (df[col]<=val[1])]
                step = f"{col} between {val[0]} and {val[1]}"
                steps.append(step)

            if op == "contains":
                if len(val) == 0:
                    continue
                df = df[df[col].str.contains('|'.join(val), na=False, case=False)]
                step = f"{col} containing any of {val}"
                steps.append(step)

            if op == "exclude":
                if len(val) == 0:
                    continue
                df = df[~df[col].str.contains('|'.join(val), na=False, case=False)]
                step = f"{col} to exclude all of {val}"
                steps.append(step)

            if op == "gte":
                df = df[df[col]>=val]
                step = f"{col} >= {val}"
                steps.append(step)

            if op == "gt":
                df = df[df[col]>val]
                step = f"{col} > {val}"
                steps.append(step)

            if op == "lte":
                df = df[df[col]<=val]
                step = f"{col} <= {val}"
                steps.append(step)

            if op == "lt":
                df = df[df[col]<val]
                step = f"{col} < {val}"
                steps.append(step)

        # generate a note with all steps
        steps = "-> " + "\n-> ".join(steps)

        return df, steps

    def _spec_focus(self, df_orig, focus):
        """
        Apply a set of focus steps to a form5500 features dataframe
        """

        steps = []
        df = df_orig.copy()

        for fcs in focus:

            name = fcs.get("name", "")

            # get the params needed
            col = fcs.get("column")
            order = fcs.get("order")
            weight = fcs.get("weight")

            # check for correctness
            if (col is None) or (order is None) or (weight is None):
                continue

            # create a normalized score (0 - 1) from the column values
            fcs_col_name = f"fcs::{col}"
            min_val = min(df[col])
            max_val = max(df[col])
            df[fcs_col_name] = (df[col] - min_val) / (max_val - min_val)

            # flip the score if the ordering is lowest-first
            if order == "asc":
                df[fcs_col_name] = 1 - df[fcs_col_name]

            # apply the weight
            df[fcs_col_name] = weight * df[fcs_col_name]

            # note the step
            step = f"Computed normalized score for {col} in {order.upper()} order and weighted by {weight}"
            steps.append(step)

        # generate the consolidated score
        cols = [c for c in df.columns if 'fcs::' in c]
        df['fcs::score'] = 0
        for c in cols:
            df['fcs::score'] = df['fcs::score'] + df[c]

        # generate a note with all steps
        steps = "-> " + "\n-> ".join(steps)

        return df, steps

    def _spec_sort(self, df_orig, sort):
        """
        Apply a sort ordering to a form5500 features dataframe
        """

        steps = []
        sort_cols = []
        sort_order = []
        df = df_orig.copy()

        for srt in sort:

            name = srt.get("name", "")

            # get the params needed
            col = srt.get("column")
            order = srt.get("order")

            # construct the sort order
            sort_cols.append(col)
            sort_order.append(True if order=="asc" else False)

            # note the step
            step = f"Sorted by {col} in {order.upper()} order"
            steps.append(step)


        # note the step for the sort by fcs::score
        step = f"Sorted by the Consolidated Weighted Normalized Score in DESC order"
        steps.append(step)

        # apply the sort order
        sort_cols.append('fcs::score')
        sort_order.append(False)
        df = df.sort_values(sort_cols, ascending=sort_order)

        # re-order columns
        first_cols = ['ACK_ID'] + sort_cols
        cols = [c for c in df.columns if c not in first_cols]
        df = df[first_cols + cols]

        # generate a note with all steps
        steps = "-> " + "\n-> ".join(steps)

        return df, steps

    def _get_steps_commentary(self, filter_steps, focus_steps, sort_steps):
        """
        Construct commentary on the steps taken
        """

        all_steps = ""

        if len(filter_steps) > 0:
            all_steps += "The Form5500s were filtered using these rules:" + "\n"
            all_steps += f"{filter_steps}" + "\n\n"
        if len(focus_steps) > 0:
            all_steps += "The Form5500s were scored using these rules:" + "\n"
            all_steps += f"{focus_steps}" + "\n"
            all_steps += "And a Consolidated Weighted Normalized Score was computed" + "\n\n"
        if len(sort_steps) > 0:
            all_steps += "The Form5500s were sorted in this order:" + "\n"
            all_steps += f"{sort_steps}" + "\n\n"

        return all_steps

    ##
    ## interfaces
    ##

    def process(self, df, spec):
        """
        Take a form5500 features dataframe and a spec
        and apply the spec to the dataframe
        """

        # check if there are columns to fill NaNs with 0
        fill_zero_cols = spec.get("focus", [])
        for column in fill_zero_cols:
            col = column.get("column")
            if col != None:
                df[col] = df[col].fillna(0)

        # apply the filters
        filter_steps = ""
        filters = spec.get("filter", [])
        if len(filters) > 0:
            df, filter_steps = self._spec_filter(df, filters)

        # apply the focus
        focus_steps = ""
        focus = spec.get("focus", [])
        if len(focus) > 0:
            df, focus_steps = self._spec_focus(df, focus)

        # apply the sort
        sort_steps = ""
        sort = spec.get("sort", [])
        if len(sort) > 0:
            df, sort_steps = self._spec_sort(df, sort)

        # construct the notes commentary
        all_steps = self._get_steps_commentary(filter_steps, focus_steps, sort_steps)

        return df, all_steps
