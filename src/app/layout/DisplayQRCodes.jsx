"use client";
import React, { useEffect, useState } from "react";
import { QrCode, Pencil, Copy } from "lucide-react";
import { useToast } from "@/components/ui/use-toast";
import { Button } from "@/components/ui/button";
import * as DialogPrimitive from "@radix-ui/react-dialog";
import EditCompoenet from './EditCompoenet'

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Loader } from "./Loader";

const DisplayQRCodes = (props) => {
 
  const { toast } = useToast();

  const copylink = (e) => {
    const link = e.currentTarget.getAttribute("link");

    navigator.clipboard.writeText(link);
    toast({
      title: `Link Coppied`,
      description: `${link}`,
      className: "text-white btnStyle border-none]",
    });
  };

  return (
    <div>
      {props.qrcodes.map((qrcode, key) => {
        return (
          <div
            key={key}
            className="pb-4 rounded-xl p-3 cardbg gap-y-6 gap-x-4 m-4 grid grid-cols-3 text-white"
          >
            <div>
              <p className="urlText text-xs">Original URL</p>
              <p className="shortenUrl">{qrcode.link_}</p>
            </div>
            <div>
              <p className="urlText text-xs">Shorten URL</p>
              <p className="shortenUrl">{qrcode.link}</p>
            </div>
            <div className="flex justify-between items-center">
              {/* qr  modal button  */}
              <Dialog>
                <DialogTrigger>
                  <QrCode />
                </DialogTrigger>
                <DialogContent className="text-white modalBg ">
                  <DialogHeader>
                    <DialogTitle>
                      <img
                        src={qrcode.qrcode_image_url}
                        width="200px"
                        height="300px"
                        alt="qr image to scan"
                        className="mx-auto"
                      />
                    </DialogTitle>
                    <DialogDescription>
                      <p className="text-green-400 text-md truncate">
                        {qrcode.qrcode_image_url}
                      </p>
                      <div className="flex justify-center gap-x-5 text-center my-5">
                        <DialogPrimitive.Close>
                          <Button className="greyBtn text-white font-bold rounded-md p-5">
                            Cancel
                          </Button>
                        </DialogPrimitive.Close>
                        <Button
                          link={qrcode.qrcode_image_url}
                          className=" greenBtn text-white font-bold rounded-md p-5"
                          onClick={copylink}
                        >
                          Copy Link
                        </Button>
                      </div>
                    </DialogDescription>
                  </DialogHeader>
                </DialogContent>
              </Dialog>

              {/* edit qrcode  */}

             <EditCompoenet qrcode={qrcode} infoFucntion={props.getUserInfo}/>

              {/* copy link  */}
              <button link={qrcode.link} variant="outline" onClick={copylink}>
                <Copy />
              </button>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default DisplayQRCodes;
