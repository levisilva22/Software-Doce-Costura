import React from 'react';

function Register() {
  return (
    <div>
      <h2>Registro</h2>
      <form>
        <div>
          <label>Nome</label>
          <input type="text" name="name" />
        </div>
        <div>
          <label>Email</label>
          <input type="email" name="email" />
        </div>
        <div>
          <label>Senha</label>
          <input type="password" name="password" />
        </div>
        <button type="submit">Registrar</button>
      </form>
    </div>
  );
}

export default Register;
