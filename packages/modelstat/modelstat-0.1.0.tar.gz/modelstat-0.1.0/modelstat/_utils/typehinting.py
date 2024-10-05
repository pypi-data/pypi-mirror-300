from typing import TypedDict, Union
from numpy import float64, int64
from numpy.typing import NDArray

__all__ = [
    "SSCPDict",
    "DOFDict",
    "ModelStatistics",
    "NDArray",
    "Union",
    "IntLike",
    "FloatLike",
    "Numeric",
]

IntLike = Union[int, int64]
FloatLike = Union[float, float64]
Numeric = Union[IntLike, FloatLike]


class DOFDict(TypedDict):
    """Statistical Degrees of Freedom

    Keys
    ----
    model : Numeric
        Model (or regression) degrees of freedom
    resid : Numeric
        Residual (or error) degrees of freedom
    total : IntLike
        Total degrees of freedom
    """

    model: Numeric
    total: IntLike
    resid: Numeric


class SSCPDict(TypedDict):
    """Sum of Squares (and Cross Products)

    Num of squares if there is only one response variable, otherwise, the sum
    of squares and cross products matrix.

    Keys
    ----
    model : Union[FloatLike, NDArray[np.float64]]
        Model (or regression)
    resid : Union[FloatLike, NDArray[np.float64]]
        Residual (or error)
    total : Union[FloatLike, NDArray[np.float64]]
        Total for the data
    """

    model: Union[FloatLike, NDArray[float64]]
    total: Union[FloatLike, NDArray[float64]]
    resid: Union[FloatLike, NDArray[float64]]


class ModelStatistics(TypedDict):
    """Primary statistics needed for model

    Keys
    ----
    dof : DOFDict
        Container for degrees of freedom from the model
    sscp : SSCPDict
        Container for the sscp matrices from the model
    """

    dof: DOFDict
    sscp: SSCPDict
