import { Loader2 } from "lucide-react"

import { Button } from "@/components/ui/button"

export function Loader() {
  return (
    <div className="p-5">

    <Button disabled  className="flex text-gray-400 mx-auto text-4xl justify-center">
      <Loader2 className="mr-2 h-4 w-4 text-4xl animate-spin" />
      Please wait
    </Button>
    </div>
  )
}
