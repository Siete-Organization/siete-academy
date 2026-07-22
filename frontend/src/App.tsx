import { Suspense, lazy } from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider } from "@/lib/auth-context";
import { Layout } from "@/components/Layout";
import { ProtectedRoute } from "@/components/ProtectedRoute";
// Login queda en el bundle inicial: es la primera pantalla de todo el mundo.
import { LoginPage } from "@/pages/auth/LoginPage";

// Code-splitting por ruta: cada página baja solo cuando se navega a ella.
// (React.lazy exige default export; adaptamos los named exports en el import.)
const lazyPage = <T extends object>(
  loader: () => Promise<T>,
  name: keyof T,
) => lazy(() => loader().then((m) => ({ default: m[name] as React.ComponentType })));

const ApplyPage = lazyPage(() => import("@/pages/apply/ApplyPage"), "ApplyPage");
const StudentDashboard = lazyPage(() => import("@/pages/student/StudentDashboard"), "StudentDashboard");
const ModulePage = lazyPage(() => import("@/pages/student/ModulePage"), "ModulePage");
const StudentFinalTest = lazyPage(() => import("@/pages/student/StudentFinalTest"), "StudentFinalTest");
const StudentModuleExam = lazyPage(() => import("@/pages/student/StudentModuleExam"), "StudentModuleExam");
const StudentFeedback = lazyPage(() => import("@/pages/student/StudentFeedback"), "StudentFeedback");
const StudentCertificate = lazyPage(() => import("@/pages/student/StudentCertificate"), "StudentCertificate");
const StudentCalendar = lazyPage(() => import("@/pages/student/StudentCalendar"), "StudentCalendar");
const StudentPostAcademy = lazyPage(() => import("@/pages/student/StudentPostAcademy"), "StudentPostAcademy");
const StudentLibrary = lazyPage(() => import("@/pages/student/StudentLibrary"), "StudentLibrary");
const StudentLibraryIndustryDetail = lazyPage(() => import("@/pages/student/StudentLibrary"), "StudentLibraryIndustryDetail");
const AccountPage = lazyPage(() => import("@/pages/account/AccountPage"), "AccountPage");
const TeacherHome = lazyPage(() => import("@/pages/teacher/TeacherHome"), "TeacherHome");
const TeacherReviews = lazyPage(() => import("@/pages/teacher/TeacherReviews"), "TeacherReviews");
const AdminApplications = lazyPage(() => import("@/pages/admin/AdminApplications"), "AdminApplications");
const AdminCohorts = lazyPage(() => import("@/pages/admin/AdminCohorts"), "AdminCohorts");
const AdminCourse = lazyPage(() => import("@/pages/admin/AdminCourse"), "AdminCourse");
const AdminPlacement = lazyPage(() => import("@/pages/admin/AdminPlacement"), "AdminPlacement");
const AdminPractica = lazyPage(() => import("@/pages/admin/AdminPractica"), "AdminPractica");
const AdminAnalytics = lazyPage(() => import("@/pages/admin/AdminAnalytics"), "AdminAnalytics");
const AdminHome = lazyPage(() => import("@/pages/admin/AdminHome"), "AdminHome");
const AdminResults = lazyPage(() => import("@/pages/admin/AdminResults"), "AdminResults");
const AdminAssessmentPreview = lazyPage(() => import("@/pages/admin/AdminAssessmentPreview"), "AdminAssessmentPreview");
const RecruiterHome = lazyPage(() => import("@/pages/recruiter/RecruiterHome"), "RecruiterHome");

function PageLoader() {
  return (
    <div className="container-editorial py-32">
      <p className="num-label">Cargando…</p>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <Layout>
        <Suspense fallback={<PageLoader />}>
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
            path="/student/module/:moduleId/exam"
            element={
              <ProtectedRoute roles={["student", "teacher", "admin"]}>
                <StudentModuleExam />
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
            path="/student/final"
            element={
              <ProtectedRoute roles={["student", "teacher", "admin"]}>
                <StudentFinalTest />
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
            path="/admin/assessments/:assessmentId/preview"
            element={
              <ProtectedRoute roles={["admin", "teacher"]}>
                <AdminAssessmentPreview />
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
        </Suspense>
      </Layout>
    </AuthProvider>
  );
}
