from rest_framework import serializers
from User_app.models import User
from Wallet_app.models import Wallet
from Wallet_app.serializers import WalletSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from DjangoProject.crypto import decrypt, encrypt

class UserSerializer(serializers.ModelSerializer):
    wallets = WalletSerializer(many=True, read_only=True)   # user have many wallets like foreign key
    profilePicture = serializers.ImageField(required=False) # manually set this field

    class Meta:
        model = User    # model name for backwards
        fields = ['id', 'firstname', 'lastname', 'email', 'personalEmail', 'phone_no', 'alternatePhone',
                  'profilePicture', 'password', 'token', 'otp', 'otpExpire', 'financialYear', 'isGoogleSignup',
                  'googleCredential', 'isDeleted', 'is_active', 'created_at', 'updated_at', 'wallets']
        extra_kwargs = {
            'password': {'write_only': True},
            'token': {'read_only': True},
        }

    def validate_email(self, value):
        """ we check user email already exists or not."""
        for user in User.objects.all():
            if decrypt(user.email) == value.lower().strip():  # decrypt DB email and compare with user's entered email
                raise serializers.ValidationError("email already exists.")
        return value

    def validate_phone_no(self, value):
        """ we check user phone already exists or not."""
        for user in User.objects.all():
            if decrypt(user.phone_no) == value:  # decrypt DB email and compare with user's entered email
                raise serializers.ValidationError("phone Number already exists.")
        return value

    ''' create a new instance of user with wallet information with user PK. '''
    def create(self, validated_data):
        # Remove profilePicture from validated_data if it's not provided
        profile_picture = validated_data.pop('profilePicture', None)
        user = User.objects.create_user(**validated_data)   # create user
        if profile_picture: # check profile picture exists
            user.profilePicture = profile_picture   # apply profile picture
            user.save() # save user profile
        ''' we decrypt user.firstname when we create user and wallet model will encrypt all data when save the data.'''
        Wallet.objects.create(user=user, name=user.decrypted_firstname, description=user.decrypted_firstname, color='#FFFFFF')   # create wallet object
        return user

    def update(self, instance, validated_data):
        # Handle profilePicture separately
        profile_picture = validated_data.pop('profilePicture', None)

        # Decrypt fields before updating
        instance.email = decrypt(instance.email) if instance.email else None
        instance.firstname = decrypt(instance.firstname) if instance.firstname else None
        instance.lastname = decrypt(instance.lastname) if instance.lastname else None
        instance.personalEmail = decrypt(instance.personalEmail) if instance.personalEmail else None
        instance.phone_no = decrypt(instance.phone_no) if instance.phone_no else None
        instance.alternatePhone = decrypt(instance.alternatePhone) if instance.alternatePhone else None
        instance.token = decrypt(instance.token) if instance.token else None
        instance.otp = decrypt(instance.otp) if instance.otp else None
        instance.otpExpire = decrypt(instance.otpExpire) if instance.otpExpire else None
        instance.financialYear = decrypt(instance.financialYear) if instance.financialYear else None
        instance.googleCredential = decrypt(instance.googleCredential) if instance.googleCredential else False

        # Prevent email and password from being updated
        if 'email' in validated_data and validated_data['email'] != instance.email:
            raise serializers.ValidationError({"email": "You cannot update the email address."})

        # Now update the fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Handle profilePicture updates
        if profile_picture:
            instance.profilePicture = profile_picture

        instance.save() # Save the updated instance, the model save method will handle encryption
        return instance

    ''' decrypted wallet object/data for passing data as response to the user '''
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for field in representation:
            if field not in ['id', 'password', 'is_active', 'created_at', 'updated_at', 'wallets', 'isDeleted',
                             'isGoogleSignup', 'profilePicture']:
                representation[field] = decrypt(representation[field])  # decrypt the field data

        # Decrypt email field for display but keep it read-only
        representation['email'] = decrypt(instance.email)

        # Handle profilePicture separately
        if instance.profilePicture:
            representation['profilePicture'] = decrypt(instance.profilePicture.name)  # decrypt the field data
        return representation


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    # validate method to check user data validation
    def validate(self, data):
        email = data.get('email')   # get email
        password = data.get('password') # get password

        try:
            # encrypt user email ande check with encrypted email of user DB.
            user = User.objects.get(email=encrypt(email))
        except User.DoesNotExist:
            raise serializers.ValidationError('No user found with this email.')

        # check user isDeleted
        if user.isDeleted:
            raise serializers.ValidationError({'error': 'User Profile is deleted.'})

        # check user password
        if not user.check_password(password):
            raise serializers.ValidationError({'error': 'Invalid Password.'})

        return {
            'user': user,
            'token': self.get_tokens_for_user(user),
        }
    # generate token for user
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }