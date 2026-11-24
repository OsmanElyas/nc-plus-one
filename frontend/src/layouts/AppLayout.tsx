import { Outlet } from "react-router"
import SiteHeader from "../components/SiteHeader"

function AppLayout() {
  return (
    <div className="app-layout">
      <SiteHeader />
      <main className="page-shell">
        <Outlet />
      </main>
      <footer className="site-footer">
        <span>NC+1</span>
        <span>Make room for one more.</span>
      </footer>
    </div>
  )
}

export default AppLayout