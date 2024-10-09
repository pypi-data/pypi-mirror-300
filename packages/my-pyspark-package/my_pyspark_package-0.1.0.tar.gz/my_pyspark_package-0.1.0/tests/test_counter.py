import unittest
from pyspark.sql import SparkSession
from hellodipesh.count_nulls_neg_ones import count_nulls_neg_ones

class TestCountNullsNegOnes(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.spark = SparkSession.builder \
            .appName("TestCountNullsNegOnes") \
            .getOrCreate()
    
    def test_count_nulls_and_neg_ones(self):
        data = [(1, -1), (2, None), (None, -1), (3, 4)]
        df = self.spark.createDataFrame(data, ["A", "B"])
        
        result_df = count_nulls_neg_ones(df).collect()
        expected = [("A", 1, 0), ("B", 1, 2)]
        
        self.assertEqual(result_df, expected)
    
    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

if __name__ == '__main__':
    unittest.main()
