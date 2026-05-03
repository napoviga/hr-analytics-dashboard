import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabaseClient'

export function useEmpleados() {
  const [empleados, setEmpleados] = useState([])
  const [errorBd, setErrorBd] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchEmpleados() {
      try {
        setLoading(true)
        const { data, error } = await supabase
          .schema('business')
          .from('v_employee_full_bynapo')
          .select('*')

        if (error) {
          setErrorBd(error.message)
          console.error("Error de Supabase:", error)
        } else {
          setEmpleados(data)
        }
      } catch (err) {
        setErrorBd(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchEmpleados()
  }, [])

  return { empleados, errorBd, loading }
}
