import streamlit as st

# List of common passwords (lowercase)
COMMON_PASSWORDS = [
    'password', '123456', '123456789', 'qwerty', 'abc123',
    'password1', 'admin', 'letmein', 'welcome', 'monkey',
    'sunshine', 'shadow', 'master', 'hello', 'freedom'
]

def check_password_strength(password):
    """Check password strength and return metrics"""
    strength = {
        'is_common': False,
        'criteria': [],
        'score': 0,
        'strength': 'Weak',
        'progress': 0
    }
    
    # Check if password is common (case-insensitive)
    strength['is_common'] = password.lower() in COMMON_PASSWORDS
    
    # Define password criteria
    criteria = [
        (len(password) >= 8, 'Minimum 8 characters'),
        (any(c.isupper() for c in password), 'At least one uppercase letter'),
        (any(c.islower() for c in password), 'At least one lowercase letter'),
        (any(c.isdigit() for c in password), 'At least one digit'),
        (any(not c.isalnum() for c in password), 'At least one special character'),
        (not strength['is_common'], 'Not a common password')
    ]
    
    # Calculate score (exclude common password check from scoring)
    strength['criteria'] = criteria
    strength['score'] = sum([int(met) for met, _ in criteria[:5]])
    
    # Determine strength level
    if strength['is_common']:
        strength['strength'] = 'Weak'
        strength['progress'] = 0
    else:
        if strength['score'] < 3:
            strength['strength'] = 'Weak'
        elif strength['score'] < 5:
            strength['strength'] = 'Medium'
        else:
            strength['strength'] = 'Strong'
        strength['progress'] = strength['score'] / 5
    
    return strength

def main():
    st.title('🔒 Password Strength Meter')
    
    # Password input with toggle visibility
    col1, col2 = st.columns([4, 1])
    with col1:
        password = st.text_input('Enter password:', type='password')
    with col2:
        show_password = st.checkbox('Show password')

    if show_password:
        st.code(f"Password entered: {password}", language="text")

    if password:
        strength = check_password_strength(password)
        
        # Display criteria checks
        st.subheader('Password Requirements:')
        for (met, label), check in zip(strength['criteria'], ['🔴', '✅']):
            status = check if met else '❌'
            st.markdown(f"{status} {label}")

        # Display strength indicator
        st.subheader('Strength Assessment:')
        if strength['strength'] == 'Weak':
            st.error('Weak Password 🔴')
        elif strength['strength'] == 'Medium':
            st.warning('Medium Password 🟡')
        else:
            st.success('Strong Password 🟢')
        
        # Show progress bar
        st.progress(strength['progress'])
        
        # Special warning for common passwords
        if strength['is_common']:
            st.error('⚠️ This password is too common and easily guessable!')

if __name__ == '__main__':
    main()