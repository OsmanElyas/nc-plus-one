import { Navigate, Outlet, useLocation } from "react-router";
import { useAuth } from "./AuthProvider";

function RequireAuth() {
  const { user, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) return <p>Checking your account...</p>;

  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <Outlet />;
}

export default RequireAuth;