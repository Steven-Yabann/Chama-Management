from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import ChamaGroup, GroupMember
from ..serializers import ChamaGroupSerializer, GroupMemberSerializer
from rest_framework.permissions import IsAuthenticated

class CreateGroupView(APIView):
    def post(self, request):
        data = request.data
        print(data)
        data['admin'] = request.user.id
        serializer = ChamaGroupSerializer(data = data)
        if serializer.is_valid():
            group = serializer.save()
            GroupMember.objects.create(user = request.user, group = group)
            return Response( serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JoinGroupView(APIView):
    def post(self, request):
        code = request.data.get('group_code')
        try:
            group = ChamaGroup.objects.get(group_code = code)
            print(group)
            GroupMember.objects.create(user = request.user, group = group)
            return Response({"message": f"Successfully joined group {group.name}"}, status=status.HTTP_200_OK)
        except ChamaGroup.DoesNotExist:
            return Response({"error": "Invalid group code"}, status=status.HTTP_400_BAD_REQUEST)
        

class GroupMembersView(APIView):
    def get(self, request, group_id):
        try:
            group = ChamaGroup.objects.get(id = group_id)
            members = GroupMember.objects.filter(group = group)
            serializer = GroupMemberSerializer(members, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ChamaGroup.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
        
class GroupDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        try:
            group = ChamaGroup.objects.get(id=group_id)

            # Check if the user is a member or admin of the group
            if request.user not in group.group_members.all() and request.user != group.admin:
                return Response({"error": "You do not have permission to view this group."}, status=status.HTTP_403_FORBIDDEN)
            print(group)
            print(group.group_members)
            serializer = ChamaGroupSerializer(group)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ChamaGroup.DoesNotExist:
            return Response({"error": "Group not found."}, status=status.HTTP_404_NOT_FOUND)