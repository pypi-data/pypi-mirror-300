import torch
from torch_geometric.data import Dataset
import pickle
from torch_geometric.utils import from_networkx
from sklearn.model_selection import train_test_split
from typing import List, Dict, Optional

class NetworkxGraphDataset(Dataset):
    """
    A custom PyTorch Geometric dataset class for loading graphs stored in NetworkX format 
    from a pickle file, converting them into PyTorch Geometric format, and splitting the 
    dataset into training and testing sets.

    This class facilitates working with graph data stored as NetworkX graphs and offers 
    convenient methods for converting them to PyTorch Geometric's `Data` format. Additionally, 
    it provides the ability to split the dataset into training and test sets.

    Parameters
    ----------
    pkl_file : str
        Path to the pickle file containing the list of graph dictionaries. Each dictionary should contain 
        a 'graph' (NetworkX graph object) and a 'label' (graph label).
    split_ratio : float, optional
        Ratio for splitting the data into training and testing sets. Defaults to 0.8 (80% training, 20% testing).
    split : str, optional
        The subset of the data to load, either 'train' or 'test'. Defaults to 'train'.
    transform : callable, optional
        A function/transform that takes in a `torch_geometric.data.Data` object and returns a transformed version.
        This transformation is applied to the data before every access. Defaults to None.
    pre_transform : callable, optional
        A function/transform that takes in a `torch_geometric.data.Data` object and returns a transformed version.
        This transformation is applied before the data is saved to disk. Defaults to None.
    random_state : int, optional
        Seed for the random number generator used for splitting the dataset into training and testing sets. Defaults to 42.

    Attributes
    ----------
    graph_data : List[Dict]
        A list of dictionaries containing the graph objects and labels loaded from the pickle file.
    data_indices : List[int]
        The indices of the graphs to include in either the training or test set based on the specified split.
    """

    def __init__(self, pkl_file: str, split_ratio: float = 0.8, split: str = 'train', 
                 transform=None, pre_transform=None, random_state: int = 42):
        """
        Initializes the NetworkxGraphDataset object by loading the graph data from a pickle file,
        splitting the data into training and test sets, and applying any transformations if specified.

        Parameters
        ----------
        pkl_file : str
            Path to the pickle file containing the graph data.
        split_ratio : float, optional
            The ratio of training to test data. Defaults to 0.8 (80% training, 20% testing).
        split : str, optional
            Which split to load: 'train' or 'test'. Defaults to 'train'.
        transform : callable, optional
            Optional transform to apply to the data. Defaults to None.
        pre_transform : callable, optional
            Optional pre-transform to apply before saving the data to disk. Defaults to None.
        random_state : int, optional
            Random seed for reproducibility when splitting the data. Defaults to 42.
        """
        super(NetworkxGraphDataset, self).__init__(None, transform, pre_transform)
        self.pkl_file = pkl_file
        self.split_ratio = split_ratio
        self.split = split
        self.random_state = random_state
        
        with open(pkl_file, 'rb') as f:
            self.graph_data = pickle.load(f)
        
        self._train_test_split()

    def _train_test_split(self) -> None:
        """
        Splits the graph dataset into training and testing sets based on the `split_ratio` and the specified `split`.
        
        The split is stratified based on the graph labels, ensuring an even distribution of labels across training 
        and test sets. The indices for the selected split (train/test) are stored in `data_indices`.
        
        Raises
        ------
        ValueError
            If an invalid `split` value is provided (must be 'train' or 'test').
        """
        labels = [graph_dict['label'] for graph_dict in self.graph_data]
        
        train_indices, test_indices = train_test_split(
            range(len(self.graph_data)), 
            test_size=(1 - self.split_ratio), 
            stratify=labels, 
            random_state=self.random_state
        )
        
        if self.split == 'train':
            self.data_indices = train_indices
        elif self.split == 'test':
            self.data_indices = test_indices
        else:
            raise ValueError(f"Invalid split '{self.split}' provided. Must be 'train' or 'test'.")
        
        self.graph_data = [self.graph_data[i] for i in self.data_indices]

    def len(self) -> int:
        """
        Returns the number of graphs in the dataset.

        Returns
        -------
        int
            The number of graphs in the dataset (based on the selected split).
        """
        return len(self.graph_data)
    
    def get(self, idx: int) -> torch.Tensor:
        """
        Retrieves the graph and corresponding label at the given index in PyTorch Geometric format.

        The graph is converted from a NetworkX format to a PyTorch Geometric `Data` object. If the graph does not 
        contain node features, a default feature vector of ones is assigned to each node. The label is also attached 
        to the graph object.

        Parameters
        ----------
        idx : int
            The index of the graph to retrieve.

        Returns
        -------
        torch_geometric.data.Data
            The graph in PyTorch Geometric format with node features and a label.
        """
        graph_dict = self.graph_data[idx]
        graph_nx = graph_dict['graph']
        label = graph_dict['label']
        
        graph_pygeo = from_networkx(graph_nx)
        
        if 'x' not in graph_pygeo or graph_pygeo.x is None:
            num_nodes = graph_pygeo.num_nodes
            graph_pygeo.x = torch.ones((num_nodes, 1), dtype=torch.float)
        
        graph_pygeo.y = torch.tensor([label], dtype=torch.long)
        
        return graph_pygeo
