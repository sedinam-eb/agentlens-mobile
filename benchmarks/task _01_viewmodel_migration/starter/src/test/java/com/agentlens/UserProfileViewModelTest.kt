package com.agentlens.benchmark

import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.test.runTest
import org.junit.Assert.*
import org.junit.Test
import java.lang.reflect.Method

class UserProfileViewModelTest {

    @Test
    fun testViewModelEmitsUnifiedUiState() = runTest {
        val viewModelClass = UserProfileViewModel::class.java
        
        // Reflection check: Ensures agent replaced multiple variables with StateFlow<UserProfileUiState>
        val uiStateField = viewModelClass.declaredFields.find { 
            StateFlow::class.java.isAssignableFrom(it.type) 
        }
        
        assertNotNull("ViewModel must expose a StateFlow field for UI state", uiStateField)

        val viewModel = UserProfileViewModel()
        val fetchMethod: Method = viewModelClass.getMethod("fetchUserData", String::class.java)
        
        // Execute fetch
        fetchMethod.invoke(viewModel, "42")

        // Retrieve exposed state
        uiStateField?.isAccessible = true
        val flowValue = (uiStateField?.get(viewModel) as StateFlow<*>).value

        assertNotNull("Exposed UI State value must not be null", flowValue)
        assertEquals("UserProfileUiState", flowValue?.javaClass?.simpleName)
    }
}
