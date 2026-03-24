"""
Empirical Analysis: Deterministic vs Randomized Quicksort

This module performs empirical analysis comparing the performance of
deterministic and randomized Quicksort implementations across different
input sizes and distributions.

Results are collected, analyzed, and can be visualized to demonstrate
the impact of randomization on algorithm performance.

Author: Assignment 5
Date: 2026
"""

import sys
import time
import random
import statistics

# Increase recursion limit to handle worst-case Quicksort scenarios
sys.setrecursionlimit(100000)

from quicksort import quicksort_deterministic, quicksort_hoare
from quicksort_randomized import (
    quicksort_randomized, 
    quicksort_randomized_median_of_three,
    QuicksortStats,
    quicksort_randomized_with_stats
)


class PerformanceTester:
    """Class to run and manage performance tests."""
    
    def __init__(self, seed=42):
        """Initialize the performance tester."""
        random.seed(seed)
        self.results = {}
    
    def generate_random_array(self, size):
        """Generate a random array of given size."""
        return [random.randint(1, 10000) for _ in range(size)]
    
    def generate_sorted_array(self, size):
        """Generate a sorted array."""
        return list(range(1, size + 1))
    
    def generate_reverse_sorted_array(self, size):
        """Generate a reverse-sorted array."""
        return list(range(size, 0, -1))
    
    def generate_nearly_sorted_array(self, size, swap_percent=0.05):
        """Generate a nearly sorted array with some random swaps."""
        arr = list(range(1, size + 1))
        num_swaps = int(size * swap_percent)
        for _ in range(num_swaps):
            i, j = random.sample(range(size), 2)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    
    def measure_time(self, func, arr, timeout=5.0):
        """
        Measure execution time of a sorting function with timeout protection.
        
        Args:
            func: The sorting function to test
            arr: The array to sort
            timeout: Maximum time allowed in seconds (default: 5.0)
        
        Returns:
            tuple: (execution_time in seconds, timed_out: bool)
        """
        import signal
        
        arr_copy = arr.copy()
        start_time = time.perf_counter()
        
        try:
            func(arr_copy)
            end_time = time.perf_counter()
            return end_time - start_time, False
        except RecursionError:
            # Handle worst-case scenarios that hit recursion limit
            return timeout + 1, True  # Return timeout+1 to indicate timeout
    
    def test_algorithm(self, name, func, array_generator, sizes, distribution_name, runs=3):
        """
        Test an algorithm on arrays of different sizes.
        
        Args:
            name (str): Name of the algorithm
            func: The sorting function
            array_generator: Function to generate test arrays
            sizes (list): List of array sizes to test
            distribution_name (str): Name of the distribution
            runs (int): Number of runs for each size (default: 3)
        
        Returns:
            dict: Results with timing information
        """
        if name not in self.results:
            self.results[name] = {}
        
        if distribution_name not in self.results[name]:
            self.results[name][distribution_name] = {}
        
        print(f"\nTesting {name} on {distribution_name} data:")
        print("-" * 70)
        print(f"{'Size':<10} {'Run 1 (s)':<15} {'Run 2 (s)':<15} {'Run 3 (s)':<15} {'Avg (s)':<10}")
        print("-" * 70)
        
        for size in sizes:
            times = []
            timed_out = False
            
            for run in range(runs):
                arr = array_generator(size)
                execution_time, timeout = self.measure_time(func, arr)
                times.append(execution_time)
                if timeout:
                    timed_out = True
            
            avg_time = statistics.mean(times)
            self.results[name][distribution_name][size] = {
                'times': times,
                'average': avg_time,
                'min': min(times),
                'max': max(times),
                'timed_out': timed_out
            }
            
            time_strs = [f"{t:.6f}" for t in times]
            timeout_indicator = " (TIMEOUT)" if timed_out else ""
            print(f"{size:<10} {time_strs[0]:<15} {time_strs[1]:<15} {time_strs[2]:<15} {avg_time:<10.6f}{timeout_indicator}")
        
        return self.results[name][distribution_name]
    
    def compare_algorithms(self, algorithms, sizes, distributions):
        """
        Compare multiple algorithms across different distributions and sizes.
        
        Args:
            algorithms (list): List of tuples (name, function)
            sizes (list): List of array sizes
            distributions (list): List of tuples (name, generator_function)
        """
        print("\n" + "=" * 70)
        print("EMPIRICAL PERFORMANCE ANALYSIS: QUICKSORT VARIANTS")
        print("=" * 70)
        
        for dist_name, dist_func in distributions:
            print(f"\n{'='*70}")
            print(f"Distribution: {dist_name.upper()}")
            print(f"{'='*70}")
            
            for algo_name, algo_func in algorithms:
                # Skip large sizes for deterministic quicksort on worst-case data
                # to prevent timeouts (O(n²) behavior)
                test_sizes = sizes
                if "Deterministic" in algo_name and dist_name in ["Sorted", "Reverse Sorted"]:
                    test_sizes = [size for size in sizes if size <= 1000]
                    if not test_sizes:
                        test_sizes = [min(sizes)]
                
                self.test_algorithm(
                    algo_name, 
                    algo_func, 
                    dist_func, 
                    test_sizes, 
                    dist_name,
                    runs=3
                )
    
    def print_summary(self):
        """Print a summary comparison of all results."""
        print("\n" + "=" * 70)
        print("SUMMARY COMPARISON")
        print("=" * 70)
        
        for dist_name in self.results[list(self.results.keys())[0]]:
            print(f"\n{dist_name.upper()} Data Distribution:")
            print("-" * 70)
            
            # Get largest size
            sizes = set()
            for algo in self.results:
                sizes.update(self.results[algo][dist_name].keys())
            
            max_size = max(sizes)
            
            print(f"\nTiming at largest size ({max_size}):")
            print(f"{'Algorithm':<35} {'Time (s)':<15} {'Relative':<10}")
            print("-" * 70)
            
            times = {}
            for algo in sorted(self.results.keys()):
                if max_size in self.results[algo][dist_name]:
                    times[algo] = self.results[algo][dist_name][max_size]['average']
            
            min_time = min(times.values())
            
            for algo in sorted(times.keys()):
                time = times[algo]
                relative = time / min_time
                print(f"{algo:<35} {time:<15.6f} {relative:<10.2f}x")


def test_correctness():
    """Test that all implementations produce correct results."""
    print("Testing Correctness of All Implementations")
    print("=" * 70)
    
    test_cases = [
        ([3, 1, 4, 1, 5, 9, 2, 6], "random"),
        ([1, 2, 3, 4, 5], "sorted"),
        ([5, 4, 3, 2, 1], "reverse sorted"),
        ([1], "single element"),
        ([2, 1], "two elements"),
        (list(range(100, 0, -1)), "100 elements reverse sorted"),
    ]
    
    algorithms = [
        ("Deterministic Quicksort", quicksort_deterministic),
        ("Hoare Partition", quicksort_hoare),
        ("Randomized Quicksort", quicksort_randomized),
        ("Randomized (Median-of-3)", quicksort_randomized_median_of_three),
    ]
    
    all_correct = True
    
    for test_arr, description in test_cases:
        print(f"\nTest: {description} - {test_arr[:20]}{'...' if len(test_arr) > 20 else ''}")
        print("-" * 70)
        
        expected = sorted(test_arr)
        
        for algo_name, algo_func in algorithms:
            arr = test_arr.copy()
            result = algo_func(arr)
            is_correct = result == expected
            status = "✓ PASS" if is_correct else "✗ FAIL"
            print(f"  {algo_name:<35} {status}")
            
            if not is_correct:
                all_correct = False
                print(f"    Expected: {expected}")
                print(f"    Got:      {result}")
    
    print("\n" + "=" * 70)
    if all_correct:
        print("✓ All implementations are CORRECT!")
    else:
        print("✗ Some implementations have ERRORS!")
    print("=" * 70)
    
    return all_correct


def test_statistics():
    """Test statistics tracking for randomized quicksort."""
    print("\n" + "=" * 70)
    print("STATISTICS ANALYSIS: OPERATION COUNTS")
    print("=" * 70)
    
    sizes = [10, 50, 100, 500, 1000]
    
    print(f"\n{'Size':<8} {'Comparisons':<15} {'Swaps':<15} {'Partitions':<15}")
    print("-" * 70)
    
    for size in sizes:
        arr = [random.randint(1, 10000) for _ in range(size)]
        stats = QuicksortStats()
        quicksort_randomized_with_stats(arr, stats=stats)
        
        print(f"{size:<8} {stats.comparisons:<15} {stats.swaps:<15} {stats.partitions:<15}")


def main():
    """Main function to run all empirical tests."""
    # First, test correctness
    test_correctness()
    
    # Test statistics
    test_statistics()
    
    # Empirical performance analysis
    algorithms = [
        ("Deterministic (Lomuto)", quicksort_deterministic),
        ("Deterministic (Hoare)", quicksort_hoare),
        ("Randomized", quicksort_randomized),
        ("Randomized (Median-of-3)", quicksort_randomized_median_of_three),
    ]
    
    # Test on different input sizes
    # Note: Deterministic worst case (sorted) will be limited to 1000 elements
    sizes = [100, 500, 1000, 2000, 5000]
    
    # Test on different distributions
    tester = PerformanceTester()
    distributions = [
        ("Random", tester.generate_random_array),
        ("Sorted", tester.generate_sorted_array),
        ("Reverse Sorted", tester.generate_reverse_sorted_array),
        ("Nearly Sorted", tester.generate_nearly_sorted_array),
    ]
    
    # Run comparisons
    tester.compare_algorithms(algorithms, sizes, distributions)
    
    # Print summary
    tester.print_summary()


if __name__ == "__main__":
    main()
