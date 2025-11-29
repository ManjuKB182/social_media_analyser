import { TopicLayout } from "../(topics)/TopicLayout";
import { DashboardShell } from "../../components/DashboardShell";

export default function TravelPage() {
  return (
    <TopicLayout>
      <DashboardShell
        topic="travel"
        title="🧳 Travel Dashboard"
        subtitle="Mirror of the Streamlit travel dashboard: state trends, top cities, categories, demographics, and Karnataka hourly trends."
      />
    </TopicLayout>
  );
}


