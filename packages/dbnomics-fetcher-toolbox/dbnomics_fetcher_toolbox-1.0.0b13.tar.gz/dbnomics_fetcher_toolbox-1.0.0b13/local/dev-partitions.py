# %%

from dbnomics_data_model.model import Dimension, DimensionValue

from dbnomics_fetcher_toolbox.partition_downloader.partitions.dimension_partition import DimensionFilter

dimensions = [
    Dimension.create(code="FREQ", values=[DimensionValue.create("A"), DimensionValue.create("M")]),
    Dimension.create(code="COUNTRY", values=[DimensionValue.create("FR"), DimensionValue.create("DE")]),
]
dimension_filter = DimensionFilter.create(dimensions=dimensions)
dimension_filter

# %%

dimension_filter.bisect()
# %%

freq_selection = dimension_filter.selected_values["FREQ"]
freq_selection

# %%

len(freq_selection.bisect()[0])

# %%
