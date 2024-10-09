"""Non-GUI functionality, including event handling, data types, and data management."""

import logging
from typing import Any

from pyqtgraph import ColorMap, colormap  # type: ignore
from qtpy.QtCore import (
    QAbstractTableModel,
    Qt,
    QModelIndex,
    QObject,
    Property,
    Signal,
    Slot,
)
from qtpy.QtGui import QColor

import pandas as pd
from pandas import DataFrame
import numpy as np
import numpy.typing as npt

log = logging.getLogger(__name__)


class DataFrameTableModel(QAbstractTableModel):
    """
    A Qt TableModel for Pandas DataFrames.

    Attributes
    ----------
    dataFrame : Property
        The DataFrame containing the models data.
    """

    def __init__(
        self,
        parent: QObject | None = None,
        dataFrame: DataFrame | None = None,
        *args,
        **kwargs,
    ):
        """
        Initialize the DataFrameTableModel.

        Parameters
        ----------
        parent : QObject, optional
            The parent object.
        dataFrame : DataFrame, optional
            The Pandas DataFrame to be represented by the model.
        *args : tuple
            Positional arguments passed to the parent class.
        **kwargs : dict
            Keyword arguments passed to the parent class.
        """
        super().__init__(parent, *args, **kwargs)
        self._dataFrame = DataFrame() if dataFrame is None else dataFrame.copy()

    def getDataFrame(self) -> DataFrame:
        """
        Get the underlying DataFrame.

        Returns
        -------
        DataFrame
            The DataFrame represented by the model.
        """
        return self._dataFrame

    def setDataFrame(self, dataFrame: DataFrame):
        """
        Set a new DataFrame.

        Parameters
        ----------
        dataFrame : DataFrame
            The new DataFrame to be set.
        """
        self.beginResetModel()
        self._dataFrame = dataFrame.copy()
        self.endResetModel()

    dataFrame = Property(DataFrame, fget=getDataFrame, fset=setDataFrame)  # type: Property
    """The DataFrame containing the models data."""

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation = Qt.Orientation.Horizontal,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any | None:
        """
        Get the header data for the specified section.

        Parameters
        ----------
        section : int
            The section index.
        orientation : Qt.Orientation, optional
            The orientation of the header. Defaults to Horizontal.
        role : int, optional
            The role of the header data. Only DisplayRole is supported at this time.

        Returns
        -------
        Any or None
            The header data.
        """
        if role == Qt.ItemDataRole.DisplayRole:
            if (
                orientation == Qt.Orientation.Horizontal
                and 0 <= section < self.columnCount()
            ):
                return self._dataFrame.columns[section]
            elif (
                orientation == Qt.Orientation.Vertical
                and 0 <= section < self.rowCount()
            ):
                return self._dataFrame.index[section]
        return None

    def rowCount(self, parent: QModelIndex | None = None) -> int:
        """
        Get the number of rows in the model.

        Parameters
        ----------
        parent : QModelIndex, optional
            The parent index.

        Returns
        -------
        int
            The number of rows.
        """
        if isinstance(parent, QModelIndex) and parent.isValid():
            return 0
        return len(self._dataFrame.index)

    def columnCount(self, parent: QModelIndex | None = None) -> int:
        """
        Get the number of columns in the model.

        Parameters
        ----------
        parent : QModelIndex, optional
            The parent index.

        Returns
        -------
        int
            The number of columns.
        """
        if isinstance(parent, QModelIndex) and parent.isValid():
            return 0
        return self._dataFrame.columns.size

    def data(
        self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole
    ) -> Any | None:
        """
        Get the data for the specified index.

        Parameters
        ----------
        index : QModelIndex
            The index of the data.
        role : int, optional
            The role of the data.

        Returns
        -------
        Any or None
            The data for the specified index.
        """
        if index.isValid() and role == Qt.ItemDataRole.DisplayRole:
            data = self._dataFrame.iloc[index.row(), index.column()]
            if isinstance(data, np.generic):
                return data.item()
            return data
        return None

    def setData(
        self, index: QModelIndex, value: Any, role: int = Qt.ItemDataRole.DisplayRole
    ) -> bool:
        """
        Set data at the specified index with the given value.

        Parameters
        ----------
        index : QModelIndex
            The index where the data will be set.
        value : Any
            The new value to be set at the specified index.
        role : int, optional
            The role of the data. Only DisplayRole is supported at this time.

        Returns
        -------
        bool
            Returns true if successful; otherwise returns false.
        """
        if index.isValid() and role == Qt.ItemDataRole.DisplayRole:
            self._dataFrame.iloc[index.row(), index.column()] = value
            self.dataChanged.emit(index, index, [role])
            return True
        return False

    def sort(self, column: int, order: Qt.SortOrder = Qt.SortOrder.AscendingOrder):
        """
        Sort the data based on the specified column and order.

        Parameters
        ----------
        column : int
            The column index to sort by.
        order : Qt.SortOrder, optional
            The sort order. Defaults to Ascending order.
        """
        if self.columnCount() == 0:
            return
        columnName = self._dataFrame.columns[column]
        self.layoutAboutToBeChanged.emit()
        self._dataFrame.sort_values(by=columnName, ascending=not order, inplace=True)
        self.layoutChanged.emit()


class ColoredDataFrameTableModel(DataFrameTableModel):
    """Extension of DataFrameTableModel providing color-mapped numerical data."""

    colormapChanged = Signal(str)  # type: Signal
    """Emitted when the colormap has been changed."""

    alphaChanged = Signal(int)  # type: Signal
    """Emitted when the alpha value has been changed."""

    _normData = DataFrame()
    _background: npt.NDArray[np.int_]
    _foreground: npt.NDArray[np.int_]
    _cmap: ColorMap = colormap.get('plasma')
    _alpha: int

    def __init__(
        self,
        parent: QObject | None = None,
        dataFrame: DataFrame | None = None,
        colormap: str = 'plasma',
        alpha: int = 255,
    ):
        """
        Initialize the ColoredDataFrameTableModel.

        Parameters
        ----------
        parent : QObject, optional
            The parent object.
        dataFrame : DataFrame, optional
            The Pandas DataFrame to be represented by the model.
        colormap : str
            The colormap to be used. Can be the name of a valid colormap from matplotlib or colorcet.
        alpha : int
            The alpha value of the colormap. Must be between 0 and 255.
        *args : tuple
            Positional arguments passed to the parent class.
        **kwargs : dict
            Keyword arguments passed to the parent class.

        """
        super().__init__(parent=parent)
        self.modelReset.connect(self._normalizeData)
        self.dataChanged.connect(self._normalizeData)
        self.colormapChanged.connect(self._defineColors)
        self.setProperty('colormap', colormap)
        self.setProperty('alpha', alpha)
        if dataFrame is not None:
            self.setDataFrame(dataFrame)

    def getColormap(self) -> str:
        """
        Return the name of the current colormap.

        Returns
        -------
        str
            The name of the current colormap
        """
        return self._cmap.name

    @Slot(str)
    def setColormap(self, name: str):
        """
        Set the colormap.

        Parameters
        ----------
        name : str
            Name of the colormap to be used. Can be the name of a valid colormap from matplotlib or colorcet.
        """
        for source in [None, 'matplotlib', 'colorcet']:
            if name in colormap.listMaps(source):
                self._cmap = colormap.get(name, source)
                self.colormapChanged.emit(name)
                return
        log.warning(f'No such colormap: "{name}"')

    colormap = Property(str, fget=getColormap, fset=setColormap, notify=colormapChanged)  # type: Property
    """The name of the colormap."""

    def getAlpha(self) -> int:
        """
        Return the alpha value of the colormap.

        Returns
        -------
        int
            The alpha value of the colormap.
        """
        return self._alpha

    @Slot(int)
    def setAlpha(self, alpha: int = 255):
        """
        Set the alpha value of the colormap.

        Parameters
        ----------
        alpha : int
            The alpha value of the colormap. Must be between 0 and 255.
        """
        _, self._alpha, _ = sorted([0, alpha, 255])
        self.alphaChanged.emit(self._alpha)
        self.layoutChanged.emit()

    alpha = Property(int, fget=getAlpha, fset=setAlpha, notify=alphaChanged)  # type: Property
    """The alpha value of the colormap."""

    def _normalizeData(self) -> None:
        """Normalize the Data for mapping to a colormap."""
        df = self._dataFrame.copy()

        # coerce non-bool / non-numeric values to numeric
        cols = df.select_dtypes(exclude=['bool', 'number']).columns
        df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')

        # normalize numeric values, avoiding inf values and division by zero
        cols = df.select_dtypes(include=['number']).columns
        df[cols].replace([np.inf, -np.inf], np.nan)
        m = df[cols].nunique() <= 1  # boolean mask for columns with only 1 unique value
        df[cols[m]] = df[cols[m]].where(df[cols[m]].isna(), other=0.0)
        cols = cols[~m]
        df[cols] = (df[cols] - df[cols].min()) / (df[cols].max() - df[cols].min())

        # convert boolean values
        cols = df.select_dtypes(include=['bool']).columns
        df[cols] = df[cols].astype(float)

        # store as property & call _defineColors()
        self._normData = df
        self._defineColors()

    def _defineColors(self) -> None:
        """
        Define the background and foreground colors according to the table's data.

        The background color is set to the colormap-mapped values of the normalized
        data, and the foreground color is set to the inverse of the background's
        approximated luminosity.

        The `layoutChanged` signal is emitted after the colors are defined.
        """
        if self._normData.empty:
            self._background = np.zeros((0, 0, 3), dtype=int)
            self._foreground = np.zeros((0, 0), dtype=int)
        else:
            m = np.isfinite(self._normData)  # binary mask for finite values
            self._background = np.ones((*self._normData.shape, 3), dtype=int) * 255
            self._background[m] = self._cmap.mapToByte(self._normData.values[m])[:, :3]
            self._foreground = 255 - (
                self._background * np.array([[[0.21, 0.72, 0.07]]])
            ).sum(axis=2).astype(int)
        self.layoutChanged.emit()

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        """
        Get the data for the specified index.

        Parameters
        ----------
        index : QModelIndex
            The index of the data.
        role : int, optional
            The role of the data.

        Returns
        -------
        Any
            The data for the specified index.
        """
        if (
            role in (Qt.ItemDataRole.BackgroundRole, Qt.ItemDataRole.ForegroundRole)
            and index.isValid()
        ):
            row = self._dataFrame.index[index.row()]
            col = index.column()
            if role == Qt.ItemDataRole.BackgroundRole:
                r, g, b = self._background[row][col]
                return QColor.fromRgb(r, g, b, self._alpha)
            if role == Qt.ItemDataRole.ForegroundRole:
                lum = self._foreground[row][col]
                return QColor('black' if (lum * self._alpha) < 32512 else 'white')
        return super().data(index, role)
