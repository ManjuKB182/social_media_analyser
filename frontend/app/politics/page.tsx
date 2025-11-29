import { TopicLayout } from "../(topics)/TopicLayout";
import { DashboardShell } from "../../components/DashboardShell";

export default function PoliticsPage() {
  return (
    <TopicLayout>
      <DashboardShell
        topic="politics"
        title="🏛️ Politics Dashboard"
        subtitle="Mirror of the Streamlit politics dashboard: state trends, cities, party-level views, demographics, and Karnataka politician hourly trends."
      />
    </TopicLayout>
  );
}


