class Menu:
    def __init__(self, menu_df):
        # menu_df is a pandas DataFrame
        self.menu_df = menu_df

    def get_categories(self):
        categories = self.menu_df["category"].unique().tolist()
        categories.sort()
        categories.insert(0, "All")
        return categories

    def filter_by_category(self, category):
        if category == "All":
            return self.menu_df
        return self.menu_df[self.menu_df["category"] == category]