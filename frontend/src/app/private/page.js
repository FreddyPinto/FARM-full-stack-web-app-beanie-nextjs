import { getSession } from "@/actions";
import { redirect } from "next/navigation";
const page = async () => {
  const session = await getSession();
  if (!session?.jwt) {
    redirect("/login");
  }
  return (
    <div className="p-4">
      <h1>Private Page</h1>
      <pre>{JSON.stringify(session, null, 2)}</pre>
    </div>
  );
};
export default page;
