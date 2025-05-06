import { useState, useEffect } from 'react';
import { getSimilarProducts } from '../services/recommendationService';
import { Box, Typography, Grid, CircularProgress } from '@mui/material';
import ProductCard from './ProductCard';

function SimilarProducts({ productId }) {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadSimilarProducts() {
      if (!productId) return;
      
      try {
        setLoading(true);
        const similarProducts = await getSimilarProducts(productId, 4);
        setProducts(similarProducts);
      } catch (error) {
        console.error('Erro ao carregar produtos similares:', error);
      } finally {
        setLoading(false);
      }
    }

    loadSimilarProducts();
  }, [productId]);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', py: 2 }}>
        <CircularProgress size={24} />
      </Box>
    );
  }

  if (products.length === 0) {
    return null;
  }

  return (
    <Box sx={{ mt: 6, mb: 4 }}>
      <Typography 
        variant="h6" 
        component="h3" 
        sx={{ mb: 2, fontWeight: 600 }}
      >
        Produtos Relacionados
      </Typography>
      <Grid container spacing={2}>
        {products.map((product) => (
          <Grid item xs={12} sm={6} md={3} key={product.product_id}>
            <ProductCard product={product} variant="compact" />
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

export default SimilarProducts;