import { TopicLayout } from "../(topics)/TopicLayout";
import { DashboardShell } from "../../components/DashboardShell";

export default function CinemaPage() {
  return (
    <TopicLayout>
      <DashboardShell
        topic="cinema"
        title="🎬 Cinema Dashboard"
        subtitle="Mirror of the Streamlit cinema dashboard: state trends, top movies, industry-wise trends, demographics, and Karnataka movie/hour trends."
      />
    </TopicLayout>
  );
}


