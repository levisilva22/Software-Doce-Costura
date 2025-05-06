import { useState, useEffect } from 'react';
import { Grid, Typography, Box, Skeleton, Divider } from '@mui/material';
import { getSimilarProducts } from '../../services/recommendationService';
import ProductCard from '../ProductCard';

const SimilarProducts = ({ productId, title = "Produtos Similares", maxItems = 4 }) => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchSimilarProducts() {
      if (!productId) return;
      
      try {
        setLoading(true);
        const similarProducts = await getSimilarProducts(productId, maxItems);
        setProducts(similarProducts);
      } catch (error) {
        console.error('Erro ao buscar produtos similares:', error);
        setProducts([]);
      } finally {
        setLoading(false);
      }
    }

    fetchSimilarProducts();
  }, [productId, maxItems]);

  if (loading) {
    return (
      <Box sx={{ mt: 4, mb: 2 }}>
        <Typography variant="h5" component="h2" gutterBottom fontWeight="bold">
          {title}
        </Typography>
        <Grid container spacing={3}>
          {[...Array(4)].map((_, index) => (
            <Grid item xs={12} sm={6} md={3} key={index}>
              <Skeleton variant="rectangular" height={200} />
              <Skeleton height={30} width="80%" sx={{ mt: 1 }} />
              <Skeleton height={20} width="60%" />
            </Grid>
          ))}
        </Grid>
      </Box>
    );
  }

  if (products.length === 0) {
    return null;
  }

  return (
    <Box sx={{ mt: 4, mb: 2 }}>
      <Typography variant="h5" component="h2" gutterBottom fontWeight="bold" color="primary.main">
        {title}
      </Typography>
      <Divider sx={{ mb: 3 }} />
      <Grid container spacing={3}>
        {products.map((product) => (
          <Grid item xs={12} sm={6} md={3} key={product.id || product.product_id}>
            <ProductCard product={product} />
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default SimilarProducts;