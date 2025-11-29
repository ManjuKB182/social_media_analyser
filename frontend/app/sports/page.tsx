import { TopicLayout } from "../(topics)/TopicLayout";
import { DashboardShell } from "../../components/DashboardShell";

export default function SportsPage() {
  return (
    <TopicLayout>
      <DashboardShell
        topic="sports"
        title="🏆 Sports Dashboard"
        subtitle="Mirror of the Streamlit sports dashboard: state trends, cities, sport-wise views, demographics, and Karnataka sport/city/hour splits."
      />
    </TopicLayout>
  );
}


