import { Loader2 } from "lucide-react"

import { Button } from "@/components/ui/button"

export function Loader() {
  return (
    <div className="p-5">

    <Button disabled  className="flex text-gray-400 mx-auto text-4xl justify-center">
      <Loader2 className="h-10 w-10 text-4xl animate-spin" />
    </Button>
    </div>
  )
}
