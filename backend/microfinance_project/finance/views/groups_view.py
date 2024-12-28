from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import ChamaGroup, GroupMember, Transaction, Savings
from ..serializers import ChamaGroupSerializer, GroupMemberSerializer, TransactionSerializer, SavingsSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

class CreateGroupView(APIView):
    def post(self, request):
        data = request.data
        print(data)
        data['admin'] = request.user.id  # Set the admin as the current user
        serializer = ChamaGroupSerializer(data=data)
        
        if serializer.is_valid():
            # Save the group
            group = serializer.save()
            
            # Automatically add the admin as the first group member
            GroupMember.objects.create(user=request.user, group=group)
            
            # Create a default savings record for the group
            Savings.objects.create(
                user=request.user,
                group=group,
                amount=0
            )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
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
            # Fetch the group
            group = get_object_or_404(ChamaGroup, id=group_id)

            # Check if the user is a member or admin of the group
            if request.user not in group.group_members.all() and request.user != group.admin:
                return Response({"error": "You do not have permission to view this group."}, status=status.HTTP_403_FORBIDDEN)
            
            print(group)
            print(group.group_members)

            # serialize group details
            group_serializer = ChamaGroupSerializer(group)

            # fetch and serialize member details
            members = GroupMember.objects.filter(group = group)
            member_serializer = GroupMemberSerializer(members, many = True)

            # fetch and serialize transaction
            transactions = Transaction.objects.filter(user__in=group.group_members.all())
            transaction_serializer = TransactionSerializer(transactions, many = True)

            # Fetch and serialize savings
            savings = Savings.objects.filter(user__in=group.group_members.all())
            savings_serializer = SavingsSerializer(savings, many=True)

            # combine data
            response_data = {
                "group_details": group_serializer.data,
                "members": member_serializer.data,
                "transactions": transaction_serializer.data,
                "savings": savings_serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        
        except ChamaGroup.DoesNotExist:
            return Response({"error": "Group not found."}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UserGroupsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Query ChamaGroup via the group_members ManyToMany relationship
            groups = ChamaGroup.objects.filter(group_members=request.user)
            
            # Convert the groups into a list of dictionaries for the response
            group_data = [{
                'groupId': group.id,
                'name': group.name,
                'description': group.description,
                'admin': group.admin.username,
            } for group in groups]

            if not group_data:
                return Response({"error": "User is not a member of any chama"}, status=status.HTTP_404_NOT_FOUND)

            return Response(group_data, status=status.HTTP_200_OK)
        except Exception as e:
            # Catch any unexpected errors
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
