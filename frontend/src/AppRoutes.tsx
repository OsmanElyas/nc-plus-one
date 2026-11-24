import { Route, Routes } from "react-router"
import AppLayout from "./layouts/AppLayout"
import AccountPage from "./pages/AccountPage"
import EventsPage from "./pages/EventsPage"
import HomePage from "./pages/HomePage"
import NotFoundPage from "./pages/NotFoundPage"

function AppRoutes() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route index element={<HomePage />} />
        <Route path="events" element={<EventsPage />} />
        <Route path="login" element={<AccountPage mode="login" />} />
        <Route path="signup" element={<AccountPage mode="signup" />} />
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  )
}

export default AppRoutes
