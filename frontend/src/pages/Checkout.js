// Crie este arquivo em /home/levi/E-commerce/frontend/src/pages/Checkout.js
import React from 'react';
import { Container, Typography, Box, Stepper, Step, StepLabel } from '@mui/material';

function Checkout() {
  const steps = ['Carrinho', 'Endereço', 'Pagamento', 'Revisão'];
  
  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 8 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Finalizar Compra
      </Typography>
      
      <Box sx={{ width: '100%', mb: 4 }}>
        <Stepper activeStep={0} alternativeLabel>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>
      </Box>
      
      <Typography>
        Implementação do checkout será feita aqui.
      </Typography>
    </Container>
  );
}

export default Checkout;