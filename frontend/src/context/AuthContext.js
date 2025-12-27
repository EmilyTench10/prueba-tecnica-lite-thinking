import { createContext, useState, useEffect, useCallback } from 'react';
import { getToken, setToken, removeToken, setRefreshToken } from '../api/token';
import { getMeApi } from '../api/auth';

export const AuthContext = createContext({
  auth: undefined,
  login: () => {},
  logout: () => {},
  loading: true,
});

export function AuthProvider({ children }) {
  const [auth, setAuth] = useState(undefined);
  const [loading, setLoading] = useState(true);

  const login = useCallback(async (accessToken, refreshToken) => {
    setToken(accessToken);
    if (refreshToken) {
      setRefreshToken(refreshToken);
    }

    try {
      const userData = await getMeApi(accessToken);
      setAuth({
        token: accessToken,
        user: userData,
      });
    } catch (error) {
      console.error('Error obteniendo datos del usuario:', error);
      removeToken();
      setAuth(null);
    }
  }, []);

  const logout = useCallback(() => {
    removeToken();
    setAuth(null);
  }, []);

  useEffect(() => {
    const validateToken = async () => {
      const token = getToken();

      if (!token) {
        setAuth(null);
        setLoading(false);
        return;
      }

      try {
        const userData = await getMeApi(token);
        setAuth({
          token,
          user: userData,
        });
      } catch (error) {
        console.error('Token inválido:', error);
        removeToken();
        setAuth(null);
      } finally {
        setLoading(false);
      }
    };

    validateToken();
  }, []);

  const contextValue = {
    auth,
    login,
    logout,
    loading,
  };

  if (loading) {
    return null;
  }

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
}
