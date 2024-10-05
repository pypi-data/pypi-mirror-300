import numpy as np
from ._utils.typehinting import NDArray, Union, IntLike, ModelStatistics

__all__ = ["get_model_statistics"]


def get_model_statistics(
    endog_true: NDArray[np.float64],
    endog_fit: NDArray[np.float64],
    se_endog_fit: Union[None, NDArray[np.float64]] = None,
    num_exog_vars: Union[IntLike, None] = None,
    weights: Union[None, NDArray[np.float64]] = None,
) -> ModelStatistics:
    """Compute model statistics

    Compute model statistics for arbitrary model. Useful when comparing the
    statistical strengths and weaknesses of different potential models in
    regression, classification, and machine learning applications.

    If provided, the residual degrees of freedom is calculated as:

            dof_resid = num_endog_vars * (num_obs - num_exog_vars - 1)

        If not provided (left as None), the residual degrees of freedom is
        calculated as:

            dof_resid = Sum_i=1 ^ num_obs 1 / se_endog_fit_i^2

    Parameters
    ----------
    endog_true : NDArray[np.np.float64]
        Training data for the endogenous/response/dependent variables
    endog_fit : NDArray[np.np.float64]
        Fitted values for the endogenous/response/dependent variables
    se_endog_fit : Union[None, NDArray[np.np.float64]]
        Standard error of fitted values for the endogenous/response/dependent
        variables, by default None. Used for calculation of residual degrees
        of freedom.
    num_exog_vars: Union[IntLike, None]
        Number of exogenouts/predictor/independent variables, by default None.
        Used for calculation of residual degrees of freedom.
    weights : Union[None, NDArray[np.np.float64]], optional
        Weights for the different observations. If uncorrelated, a 1darray for
        each weight, if correlated, a 2darray indicating correlation between
        multiple values, if no weighting was needed, then leave as None, by
        default None

    Returns
    -------
    ModelStatistics
        Dictionary containing the degrees of freedom, and sum squares and
        products for the model (regression), residuals (error), and total values

    Raises
    ------
    ValueError
        Shape of endog_true, endog_fit, and se_endog_fit (if provided) are
        unequal
    ValueError
        Weights contain incorrect shape or number of values. If the weights are
        provided as a vector/1darray, there must be the same number of elements
        as there are observations. If provided as a matrix/2darray, it must be
        square with number of rows and columns equal to the number of
        observations. It cannot be higher dimension than 2.
    ValueError
        Raised if any of the weights are negative. Weights must be positive.
    """
    n_obs, n_endog = endog_true.shape

    if endog_fit.shape != (n_obs, n_endog):
        raise ValueError(
            "endog_fit, exog_fit, and se_endog_fit must all have the same shape"
        )
    if se_endog_fit is None:
        use_num_exog = True
    elif num_exog_vars is None:
        raise ValueError(
            (
                "Either of num_exog_vars or se_endog_fit must be provided in "
                "order to compute the residual degrees of freedom"
            )
        )
    else:
        use_num_exog = False
    if weights is None:
        weights = np.eye(n_obs, dtype=np.float64)
    elif weights.ndim == 1:
        if (
            weights.shape == (n_obs,)
            or weights.shape == (n_obs, 1)
            or weights.shape == (1, n_obs)
        ):
            weights = np.diag(weights.flatten())
        else:
            raise ValueError(
                "Vector of weights must have number of elements equaling number of observations"
            )
    elif weights.ndim == 2 and weights.shape != (n_obs, n_obs):
        raise ValueError(
            "Matrix of weights must be n-by-n in which n is the number of observations"
        )
    else:
        raise ValueError("Weights must either be one dimensional or two dimensional")
    if np.any(weights < 0.0):
        raise ValueError("None of the weights can be negative")

    weights *= n_obs / np.sum(weights)
    residuals: NDArray[np.float64] = endog_true - endog_fit

    SSCP_total: NDArray[np.float64] = endog_true.T @ weights @ endog_true
    SSCP_resid: NDArray[np.float64] = residuals.T @ weights @ residuals
    SSCP_model: NDArray[np.float64] = SSCP_total - SSCP_resid

    dof_total = n_obs - 1
    dof_resid = np.sum(1.0 / (se_endog_fit**2))
    dof_model = dof_total - dof_resid

    return {
        "dof": {"model": dof_model, "resid": dof_resid, "total": dof_total},
        "sscp": {"model": SSCP_model, "resid": SSCP_resid, "total": SSCP_total},
    }
