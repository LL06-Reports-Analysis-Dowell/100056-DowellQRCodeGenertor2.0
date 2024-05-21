from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import QRCode, QRCodeClone, QRCodeVersion
from .serializers import QRCodeSerializer, QRCodeCloneSerializer, QRCodeVersionSerializer, MasterLink, MasterLinkSerializer

class QRCodeAPIView(APIView):

    def get_qrcode(self, pk):
        try:
            return QRCode.objects.get(pk=pk)
        except QRCode.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        if pk:
            qrcode = self.get_qrcode(pk)
            if qrcode.is_finalized:
                return Response({'message': 'QR code is finalized and can no longer be used'}, status=status.HTTP_403_FORBIDDEN)
            if not qrcode.is_open:
                return Response({'message': 'QR code is closed and cannot be opened again'}, status=status.HTTP_403_FORBIDDEN)
            serializer = QRCodeSerializer(qrcode)
            return Response(serializer.data)
        else:
            qrcodes = QRCode.objects.all()
            serializer = QRCodeSerializer(qrcodes, many=True)
            return Response(serializer.data)

    def post(self, request, pk=None):
        if pk:
            action = request.data.get('action')
            if action == 'activate':
                return self.activate_qrcode(request, pk)
            elif action == 'update_data':
                return self.update_qrcode_data(request, pk)
            elif action == 'finalize':
                return self.finalize_qrcode(request, pk)
            elif action == 'open':
                return self.open_qrcode(request, pk)
            else:
                return Response({'message': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            num_qrcodes = request.data.get('num_qrcodes', 1)
            qrcodes = []

            for _ in range(num_qrcodes):
                serializer = QRCodeSerializer(data=request.data)
                if serializer.is_valid():
                    qrcode = serializer.save()
                    qrcodes.append(qrcode)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(QRCodeSerializer(qrcodes, many=True).data, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        qrcode = self.get_qrcode(pk)
        if qrcode.is_finalized:
            return Response({'message': 'QR code is finalized and cannot be updated'}, status=status.HTTP_403_FORBIDDEN)
        serializer = QRCodeSerializer(qrcode, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        qrcode = self.get_qrcode(pk)
        qrcode.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def activate_qrcode(self, request, pk):
        qrcode = self.get_qrcode(pk)
        if qrcode.is_finalized:
            return Response({'message': 'QR code is finalized and cannot be activated'}, status=status.HTTP_403_FORBIDDEN)

        num_clones = request.data.get('num_clones', 1)
        clones = []

        for _ in range(num_clones):
            clone = QRCodeClone.objects.create(original_qrcode=qrcode, data=qrcode.data)
            clones.append(clone)

        qrcode.is_active = True
        qrcode.save()

        return Response({
            'message': 'QR code activated',
            'clones': QRCodeCloneSerializer(clones, many=True).data
        }, status=status.HTTP_200_OK)

    def update_qrcode_data(self, request, pk):
        qrcode = self.get_qrcode(pk)
        if qrcode.is_finalized:
            return Response({'message': 'QR code is finalized and cannot be updated'}, status=status.HTTP_403_FORBIDDEN)

        new_data = request.data.get('data')

        if new_data:
            latest_version_number = qrcode.versions.count() + 1
            QRCodeVersion.objects.create(qrcode=qrcode, data=new_data, version_number=latest_version_number)

            qrcode.data = new_data
            qrcode.save()

            return Response({'message': 'QR code updated'}, status=status.HTTP_200_OK)
        return Response({'message': 'No data provided'}, status=status.HTTP_400_BAD_REQUEST)

    def finalize_qrcode(self, request, pk):
        qrcode = self.get_qrcode(pk)
        qrcode.is_finalized = True
        qrcode.is_open = False  # Optionally close the QR code when finalizing
        qrcode.save()
        return Response({'message': 'QR code finalized and closed'}, status=status.HTTP_200_OK)

    def open_qrcode(self, request, pk):
        qrcode = self.get_qrcode(pk)
        if qrcode.is_finalized:
            return Response({'message': 'QR code is finalized and cannot be opened again'}, status=status.HTTP_403_FORBIDDEN)

        qrcode.is_open = True
        qrcode.save()
        return Response({'message': 'QR code opened'}, status=status.HTTP_200_OK)



class MasterLinkListCreateView(APIView):
    def get(self, request):
        master_links = MasterLink.objects.all()
        serializer = MasterLinkSerializer(master_links, many=True)
        return Response(serializer.data)

    def post(self, request):
        num_qrcodes = request.data.get('num_qrcodes', 1)
        master_link_name = request.data.get('name', 'MasterLink')
        qrcodes = []

        for _ in range(num_qrcodes):
            qrcode = QRCode.objects.create(data=request.data.get('data', ''))
            qrcodes.append(qrcode)

        master_link = MasterLink.objects.create(name=master_link_name)
        master_link.qrcodes.set(qrcodes)
        master_link.save()

        # Generate the HTTP master link
        master_link.link = f"http://example.com/masterlinks/{master_link.id}/qrcodes"
        master_link.save()

        return Response(MasterLinkSerializer(master_link).data, status=status.HTTP_201_CREATED)