import gymnasium as gym
import numpy as np
from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, Optional, Dict, Any, Tuple
from ..feed import IFeeder

class TradeEnv(gym.Env, ABC):
    """
    Custom OpenAI Gym environment for simulating spot market trading.

    This environment simulates trading strategies by interacting with market data, managing 
    an account's balance, and executing buy/sell actions. It uses a data feeder for market data 
    and an account management system for handling transactions.

    Attributes:
        _feeder (IFeeder): Feeder for providing market data.
        _account_class (Callable): Callable for managing the trading account.
        _account (Optional[object]): Current trading account instance.
        _action (Enum): Enumeration of possible trading actions (e.g., BUY, SELL, HOLD).
        _balance (int): Initial balance for trading.
        _buy_quantity (int): Number of assets bought per transaction.
        _fee (float): Transaction fee as a percentage.
        _tax (float): Tax on sales as a percentage.
        _is_terminated (bool): Whether the episode has terminated.
        _is_truncated (bool): Whether the episode has been truncated.
        action_space (gym.spaces.Discrete): Action space for trading actions.
        observation_space (gym.spaces.Box): Observation space for market data.
    """

    def __init__(
        self, 
        feeder: IFeeder,
        account: Callable = None,
        action: Enum = None,
        balance: int = 1_000_000,
        buy_quantity: int = 10,
        fee: float = 0.3,
        tax: float = 0.38
    ) -> None:
        """
        Initializes the trading environment.

        Args:
            feeder (IFeeder): Data feeder for market data.
            account (Callable, optional): Callable to manage the trading account. Defaults to None.
            action (Enum, optional): Enum for possible trading actions. Defaults to None.
            balance (int, optional): Starting balance for trading. Defaults to 1,000,000.
            buy_quantity (int, optional): Number of assets to buy per trade. Defaults to 10.
            fee (float, optional): Transaction fee as a percentage. Defaults to 0.3.
            tax (float, optional): Tax on sales as a percentage. Defaults to 0.38.
        """
        super().__init__()

        feeder.reset()
        self._feeder = feeder
        self._account_class = account
        self._account = None
        self._accounts = []
        self._action = action
        self._balance = balance
        self._buy_quantity = buy_quantity
        self._fee = fee
        self._tax = tax
        self._is_terminated = False
        self._is_truncated = False
        
        self.action_space = gym.spaces.Discrete(len(action))
        self.observation_space = gym.spaces.Box(
            low=-np.inf, high=np.inf, shape=self._feeder.partShape(), dtype=np.float32
        )

    def getFeeder(self) -> IFeeder:
        """
        Returns the data feeder.

        Returns:
            IFeeder: The data feeder.
        """
        return self._feeder
    
    def getAccount(self) -> Optional[object]:
        """
        Returns the current trading account.

        Returns:
            Optional[object]: Current trading account, or None if not initialized.
        """
        return self._account
    
    def getAccounts(self) -> list:
        """
        Returns the list of all past accounts.

        Returns:
            list: List of past account states.
        """
        return self._accounts
    
    def getHistory(self) -> Tuple[Any, Any]:
        """
        Returns the history of assets and trades.

        Returns:
            Tuple[Any, Any]: Asset and trade history as DataFrames.
        """
        return self._account.getHistory()
    
    def reset(
        self, 
        seed: Optional[int] = None, 
        options: Optional[Dict[str, Any]] = None
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Resets the environment to the initial state.

        Args:
            seed (Optional[int], optional): Random seed. Defaults to None.
            options (Optional[Dict[str, Any]], optional): Reset options. Defaults to None.

        Returns:
            Tuple[np.ndarray, Dict[str, Any]]: Initial observation and additional info.
        """
        super().reset(seed=seed)

        if seed is not None:
            np.random.seed(seed)
        
        self._feeder.reset()
        feed_info = self._feeder.info()
        code, name = "test", "test"
        if feed_info is not None:
            code = feed_info["code"] if "code" in feed_info else "test"
            name = feed_info["name"] if "name" in feed_info else "test"
        self._account = self._account_class(
            code, name, balance=self._balance, fee=self._fee, tax=self._tax
        )
        self._is_terminated = False
        self._is_truncated = False
        self._accounts = []
        
        self._obs, self._feed_change = self._feeder.next()
        self._account.hold(
            self._obs[0][self._feeder.col_daytime()],
            self._obs[0][self._feeder.col_price()]
        )
        return self._obs, self._extra_infos(self._obs)
    
    def _extra_infos(self, obs: np.ndarray) -> Dict[str, Any]:
        """
        Returns additional information about the current state.

        Args:
            obs (np.ndarray): Current observation.

        Returns:
            Dict[str, Any]: Additional info including asset and trade history.
        """
        hist_asset, hist_trade = self.getHistory()
        self._cant_trade = False
        if (
            hist_asset[0].balance < obs[0][self._feeder.col_price()] 
            and hist_asset[0].quantity == 0
        ):
            self._cant_trade = True
        return {
            "feed_change": self._feed_change,
            "asset": hist_asset[0] if len(hist_asset) > 0 else None,
            "trade": hist_trade[0] if len(hist_trade) > 0 else None,
        }
    
    def _terminated(self, obs: Optional[np.ndarray], feed_change: Optional[object]) -> bool:
        """
        Checks if the episode is terminated.

        Args:
            obs (Optional[np.ndarray]): Current observation.
            feed_change (Optional[object]): Data feed change.

        Returns:
            bool: True if terminated, False otherwise.
        """
        return obs is None and feed_change is None
    
    def _truncated(self, obs: Optional[np.ndarray], feed_change: Optional[object]) -> bool:
        """
        Checks if the episode is truncated.

        Args:
            obs (Optional[np.ndarray]): Current observation.
            feed_change (Optional[object]): Data feed change.

        Returns:
            bool: True if truncated, False otherwise.
        """
        return self._cant_trade
    
    @abstractmethod
    def _act(
        self, 
        action: int, 
        rate: float, 
        obs: np.ndarray, 
        feed_change: object
    ) -> None:
        """
        Executes the specified action.

        Args:
            action (int): Action to perform.
            rate (float): Rate that may influence the action.
            obs (np.ndarray): Current observation.
            feed_change (object): Data feed change.

        Raises:
            NotImplementedError: If not implemented in subclass.
        """
        pass
    
    @abstractmethod
    def _reward(
        self, 
        action: int, 
        rate: float, 
        obs: np.ndarray, 
        feed_change: object, 
        asset: Optional[object], 
        trade: Optional[object]
    ) -> float:
        """
        Calculates the reward for the action taken.

        Args:
            action (int): Action taken.
            rate (float): Rate that may influence the reward.
            obs (np.ndarray): Current observation after action.
            feed_change (object): Data feed change after action.
            asset (Optional[object]): Latest asset history.
            trade (Optional[object]): Latest trade history.

        Returns:
            float: The calculated reward.
        """
        return 0.0
    
    def step(self, action: int, rate: float = 0.0) -> Tuple[np.ndarray, float, bool, bool, Optional[Dict[str, Any]]]:
        """
        Executes one step in the environment.

        Args:
            action (int): Action to take.
            rate (float, optional): Rate influencing the action. Defaults to 0.0.

        Returns:
            Tuple[np.ndarray, float, bool, bool, Optional[Dict[str, Any]]]: 
                - Observation after step
                - Reward
                - Termination flag
                - Truncation flag
                - Additional info
        """
        if self._is_terminated:
            return self._obs, 0.0, self._is_terminated, self._is_truncated, None
        
        self._act(action, rate, self._obs, self._feed_change)
        self._obs, self._feed_change = self._feeder.next()

        self._is_terminated = self._terminated(self._obs, self._feed_change)
        truncated = self._truncated(self._obs, self._feed_change)
        if self._is_terminated or truncated:
            return self._obs, 0.0, self._is_terminated, self._is_truncated, None
        
        extra_info = self._extra_infos(self._obs)
        if extra_info["feed_change"]:
            self._accounts.append(self._account)
            feed_info = self._feeder.info()
            self._account = self._account_class(
                feed_info["code"], feed_info["name"], balance=self._balance, fee=self._fee, tax=self._tax
            )
            self._obs, self._feed_change = self._feeder.next()
            self._account.hold(
                self._obs[0][self._feeder.col_daytime()],
                self._obs[0][self._feeder.col_price()]
            )

            return self._obs, 0.0, self._is_terminated, True, None
        
        reward = self._reward(
            action, rate, self._obs, self._feed_change, 
            extra_info["asset"], extra_info["trade"]
        )

        return self._obs, reward, self._is_terminated, truncated, extra_info
