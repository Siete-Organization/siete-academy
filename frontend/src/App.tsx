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
import { TeacherReviews } from "@/pages/teacher/TeacherReviews";
import { AdminApplications } from "@/pages/admin/AdminApplications";
import { AdminCohorts } from "@/pages/admin/AdminCohorts";
import { AdminPlacement } from "@/pages/admin/AdminPlacement";
import { AdminAnalytics } from "@/pages/admin/AdminAnalytics";
import { AdminHome } from "@/pages/admin/AdminHome";
import { RecruiterHome } from "@/pages/recruiter/RecruiterHome";
import { HomePage } from "@/pages/HomePage";

export default function App() {
  return (
    <AuthProvider>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
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
            path="/student/certificate"
            element={
              <ProtectedRoute roles={["student"]}>
                <StudentCertificate />
              </ProtectedRoute>
            }
          />

          <Route
            path="/teacher"
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
            path="/admin/placement"
            element={
              <ProtectedRoute roles={["admin"]}>
                <AdminPlacement />
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
