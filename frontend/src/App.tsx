import { Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider } from "@/lib/auth-context";
import { Layout } from "@/components/Layout";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { ApplyPage } from "@/pages/apply/ApplyPage";
import { LoginPage } from "@/pages/auth/LoginPage";
import { StudentDashboard } from "@/pages/student/StudentDashboard";
import { ModulePage } from "@/pages/student/ModulePage";
import { StudentFeedback } from "@/pages/student/StudentFeedback";
import { StudentCertificate } from "@/pages/student/StudentCertificate";
import { StudentCalendar } from "@/pages/student/StudentCalendar";
import { StudentPostAcademy } from "@/pages/student/StudentPostAcademy";
import {
  StudentLibrary,
  StudentLibraryIndustryDetail,
} from "@/pages/student/StudentLibrary";
import { AccountPage } from "@/pages/account/AccountPage";
import { TeacherHome } from "@/pages/teacher/TeacherHome";
import { TeacherReviews } from "@/pages/teacher/TeacherReviews";
import { AdminApplications } from "@/pages/admin/AdminApplications";
import { AdminCohorts } from "@/pages/admin/AdminCohorts";
import { AdminCourse } from "@/pages/admin/AdminCourse";
import { AdminPlacement } from "@/pages/admin/AdminPlacement";
import { AdminPractica } from "@/pages/admin/AdminPractica";
import { AdminAnalytics } from "@/pages/admin/AdminAnalytics";
import { AdminHome } from "@/pages/admin/AdminHome";
import { AdminResults } from "@/pages/admin/AdminResults";
import { RecruiterHome } from "@/pages/recruiter/RecruiterHome";

export default function App() {
  return (
    <AuthProvider>
      <Layout>
        <Routes>
          <Route path="/" element={<LoginPage />} />
          <Route path="/apply" element={<ApplyPage />} />
          <Route path="/login" element={<LoginPage />} />

          <Route
            path="/student"
            element={
              <ProtectedRoute roles={["student"]}>
                <StudentDashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/student/module/:moduleId"
            element={
              <ProtectedRoute roles={["student"]}>
                <ModulePage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/student/feedback"
            element={
              <ProtectedRoute roles={["student"]}>
                <StudentFeedback />
              </ProtectedRoute>
            }
          />
          <Route
            path="/student/calendar"
            element={
              <ProtectedRoute roles={["student"]}>
                <StudentCalendar />
              </ProtectedRoute>
            }
          />
          <Route
            path="/student/certificate"
            element={
              <ProtectedRoute roles={["student"]}>
                <StudentCertificate />
              </ProtectedRoute>
            }
          />
          <Route
            path="/student/post-academy"
            element={
              <ProtectedRoute roles={["student"]}>
                <StudentPostAcademy />
              </ProtectedRoute>
            }
          />
          <Route
            path="/student/library"
            element={
              <ProtectedRoute roles={["student"]}>
                <StudentLibrary />
              </ProtectedRoute>
            }
          />
          <Route
            path="/student/library/industries/:slug"
            element={
              <ProtectedRoute roles={["student"]}>
                <StudentLibraryIndustryDetail />
              </ProtectedRoute>
            }
          />
          <Route
            path="/account"
            element={
              <ProtectedRoute roles={["student", "teacher", "admin", "recruiter"]}>
                <AccountPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/teacher"
            element={
              <ProtectedRoute roles={["teacher", "admin"]}>
                <TeacherHome />
              </ProtectedRoute>
            }
          />
          <Route
            path="/teacher/reviews"
            element={
              <ProtectedRoute roles={["teacher", "admin"]}>
                <TeacherReviews />
              </ProtectedRoute>
            }
          />

          <Route
            path="/admin"
            element={
              <ProtectedRoute roles={["admin"]}>
                <AdminHome />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/applications"
            element={
              <ProtectedRoute roles={["admin"]}>
                <AdminApplications />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/cohorts"
            element={
              <ProtectedRoute roles={["admin"]}>
                <AdminCohorts />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/course"
            element={
              <ProtectedRoute roles={["admin", "teacher"]}>
                <AdminCourse />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/placement"
            element={
              <ProtectedRoute roles={["admin"]}>
                <AdminPlacement />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/practica"
            element={
              <ProtectedRoute roles={["admin"]}>
                <AdminPractica />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/analytics"
            element={
              <ProtectedRoute roles={["admin"]}>
                <AdminAnalytics />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/results"
            element={
              <ProtectedRoute roles={["admin", "teacher"]}>
                <AdminResults />
              </ProtectedRoute>
            }
          />

          <Route
            path="/recruiter"
            element={
              <ProtectedRoute roles={["recruiter", "admin"]}>
                <RecruiterHome />
              </ProtectedRoute>
            }
          />

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Layout>
    </AuthProvider>
  );
}
