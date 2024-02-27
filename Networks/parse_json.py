df = pd.read_csv("./bitcoin.csv", index_col=False)
print(len(df))
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 10)
df = df[
    [
        "rank",
        "exchangeId",
        "exchangeName",
        "exchangeSlug",
        "volumePercent",
        "volumeQuote",
        "isVerified",
        "marketUrl",
        "effectiveLiquidity",
        "lastUpdated",
        "marketPair",
        "price",
    ]
]
df = df[(df["isVerified"] == 1) & (df["volumePercent"] > 0.01) & (df["rank"] < 10000)]

grouped = df.groupby("marketPair")

min_indices = grouped["price"].idxmin()
max_indices = grouped["price"].idxmax()

min_exchange_names = df.loc[min_indices, "exchangeName"].values
max_exchange_names = df.loc[max_indices, "exchangeName"].values

result_df = pd.DataFrame(
    {
        "marketPair": grouped["marketPair"].first(),
        "minPrice": df.loc[min_indices, "price"].values,
        "minExchangeName": min_exchange_names,
        "maxPrice": df.loc[max_indices, "price"].values,
        "maxExchangeName": max_exchange_names,
    }
)
result_df = result_df.drop_duplicates().reset_index(drop=True)
result_df.to_csv("./data/bitcoin.csv")
