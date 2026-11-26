import { Route, Routes } from "react-router"
import AppLayout from "./layouts/AppLayout"
import AccountPage from "./pages/AccountPage"
import EventDetailPage from "./pages/EventDetailPage"
import EventsPage from "./pages/EventsPage"
import HomePage from "./pages/HomePage"
import NotFoundPage from "./pages/NotFoundPage"
import RequireAuth from "./auth/RequireAuth"
import MyEventsPage from "./pages/MyEventsPage"

function AppRoutes() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route index element={<HomePage />} />
        <Route path="events" element={<EventsPage />} />
        <Route path="events/:eventId" element={<EventDetailPage />} />
        <Route path="login" element={<AccountPage mode="login" />} />
        <Route path="signup" element={<AccountPage mode="signup" />} />
        <Route path="*" element={<NotFoundPage />} />
        <Route element={<RequireAuth />}>
        <Route path="my-events" element={<MyEventsPage />} />
        </Route>
      </Route>
    </Routes>
  )
}

export default AppRoutes
