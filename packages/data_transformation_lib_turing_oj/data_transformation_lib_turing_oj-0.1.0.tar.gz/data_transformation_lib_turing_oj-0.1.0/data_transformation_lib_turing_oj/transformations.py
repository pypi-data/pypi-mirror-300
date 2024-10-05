import numpy as np


def transpose2d(input_matrix: list[list[float]]) -> list[list[float]]:
    """
    Transpose a 2D matrix (swap rows and columns).

    Parameters:
    input_matrix (list[list[float]]): The 2D matrix to transpose.

    Returns:
    list[list[float]]: The transposed matrix.
    """
    transposed_matrix = [list(row) for row in zip(*input_matrix)]
    return transposed_matrix


def window1d(input_array: list, size: int, shift: int = 1, stride: int = 1) -> list[list]:
    """
    Generate sliding windows from a 1D array.

    Parameters:
    input_array (list): The input 1D array.
    size (int): The size of each sliding window.
    shift (int, optional): The step size for shifting the window. Default is 1.
    stride (int, optional): The step size for selecting elements within each window. Default is 1.

    Returns:
    list[list]: A list of 1D arrays representing the sliding windows.
    """
    if isinstance(input_array, list):
        input_array = np.array(input_array)

    windows = []
    for start in range(0, len(input_array) - size + 1, shift):
        window = input_array[start:start + size:stride]
        windows.append(window.tolist())

    return windows


def convolution2d(input_matrix: np.ndarray, kernel: np.ndarray, stride: int = 1) -> np.ndarray:
    """
    Perform 2D cross-correlation on an input matrix using a specified kernel and stride.

    Parameters:
    input_matrix (np.ndarray): 2D array of real numbers.
    kernel (np.ndarray): 2D array representing the kernel.
    stride (int): Step size for sliding the kernel. Must be > 0.

    Returns:
    np.ndarray: Resulting 2D array after applying cross-correlation.
    """
    if stride <= 0:
        raise ValueError("Stride must be a positive integer.")
        
    # Get dimensions of the input and kernel
    input_height, input_width = input_matrix.shape
    kernel_height, kernel_width = kernel.shape
    
    # Calculate output dimensions
    output_height = (input_height - kernel_height) // stride + 1
    output_width = (input_width - kernel_width) // stride + 1
    
    # Initialize the output matrix with zeros
    output_matrix = np.zeros((output_height, output_width))
    
    # Perform cross-correlation
    for i in range(0, output_height):
        for j in range(0, output_width):
            # Calculate the starting indices for the current window
            start_i = i * stride
            start_j = j * stride
            
            # Extract the current window from the input matrix
            window = input_matrix[start_i:start_i + kernel_height, start_j:start_j + kernel_width]
            
            # Perform the element-wise multiplication and sum the result
            output_matrix[i, j] = np.sum(window * kernel)
    
    return output_matrix

